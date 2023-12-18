from .modeling_lsg_pegasus import *
try:
    from ..conversion_utils import ConversionScript
except:
    from conversion_utils import ConversionScript

class PegasusConversionScript(ConversionScript):

    _ARCHITECTURE_TYPE_DICT = {
        "PegasusModel": ("LSGPegasusModel", LSGPegasusModel),
        "PegasusForCausalLM": ("LSGPegasusForCausalLM", LSGPegasusForCausalLM),
        "PegasusForConditionalGeneration": ("LSGPegasusForConditionalGeneration", LSGPegasusForConditionalGeneration),
    }
    _ARCHITECTURE_TYPE_DICT = {**{"LSG" + k: v for k, v in _ARCHITECTURE_TYPE_DICT.items()}, **_ARCHITECTURE_TYPE_DICT}

    _BASE_ARCHITECTURE_TYPE = "PegasusModel"
    _DEFAULT_ARCHITECTURE_TYPE = "PegasusForConditionalGeneration"
    _CONFIG_MODULE = LSGPegasusConfig

    _DEFAULT_CONFIG_POSITIONAL_OFFSET = 0
    _DEFAULT_POSITIONAL_OFFSET = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_module(self, model, is_base_architecture):
        if is_base_architecture:
            return model
        return model.model

    def update_global_randomly(self, module_prefix, bos_id, stride, keep_first_global):

        import torch
        from torch.distributions.multivariate_normal import MultivariateNormal

        u = module_prefix.shared.weight.clone()
        cov = torch.cov(u.T)
        m = MultivariateNormal(u.mean(dim=0), cov)
        w = m.sample((512,))
        
        w[0] = u[bos_id]
        positions = module_prefix.encoder.embed_positions.weight.clone()
        positions = self.order_positions(positions, stride)

        if keep_first_global:
            module_prefix.encoder.global_embeddings.weight.data[1:] = (w + positions)[1:]
        else:
            module_prefix.encoder.global_embeddings.weight.data = w + positions

    def update_global(self, module_prefix, bos_id, mask_id, stride, keep_first_global):

        u = module_prefix.shared.weight.clone()
        positions = module_prefix.encoder.embed_positions.weight.clone()
        positions = self.order_positions(positions, stride)
        
        positions[0] += u[bos_id]
        positions[1:] += u[mask_id].unsqueeze(0)

        if keep_first_global:
            module_prefix.encoder.global_embeddings.weight.data[1:] = positions[1:]
        else:
            module_prefix.encoder.global_embeddings.weight.data = positions

    def update_positions_with_model(self, model, max_pos):
        model.resize_position_embeddings(max_pos)

    def run_test(self):
        
        from transformers import AutoConfig, AutoTokenizer

        initial_path = self.initial_model
        lsg_path = self.model_name

        config = AutoConfig.from_pretrained(lsg_path, trust_remote_code=True)
        tokenizer = AutoTokenizer.from_pretrained(lsg_path)
        text = f"Paris is the {tokenizer.mask_token} of France."

        max_length = config.max_position_embeddings - 20
        hidden_size = config.hidden_size

        self.run_models(lsg_path, max_length, hidden_size, text, AUTO_MAP, is_encoder_decoder=True)
        self.run_pipeline(lsg_path, initial_path, tokenizer, text)

    def run_pipeline(self, lsg_path, initial_path, tokenizer, text):

        from transformers import AutoModelForSeq2SeqLM, pipeline

        model = AutoModelForSeq2SeqLM.from_pretrained(lsg_path, trust_remote_code=True)
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
        pipe_lsg = pipe(text)

        model = AutoModelForSeq2SeqLM.from_pretrained(initial_path, trust_remote_code=True)
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
        pipe_initial = pipe(text)
  
        print("\n\n" + "="*5 + " LSG PIPELINE " + "="*5 + "\n")
        print(text)
        print(pipe_lsg[0])
        print("\n\n" + "="*5 + " INITIAL PIPELINE " + "="*5 + "\n")
        print(text)
        print(pipe_initial[0])