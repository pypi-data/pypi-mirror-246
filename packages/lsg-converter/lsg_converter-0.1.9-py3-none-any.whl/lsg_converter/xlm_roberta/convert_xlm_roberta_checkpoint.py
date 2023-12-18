from .modeling_lsg_xlm_roberta import *
try:
    from ..conversion_utils import ConversionScript
except:
    from conversion_utils import ConversionScript

class XLMRobertaConversionScript(ConversionScript):

    _ARCHITECTURE_TYPE_DICT = {
        "XLMRobertaModel": ("LSGXLMRobertaModel", LSGXLMRobertaModel),
        "XLMRobertaForMaskedLM": ("LSGXLMRobertaForMaskedLM", LSGXLMRobertaForMaskedLM),
        "XLMRobertaForCausalLM": ("LSGXLMRobertaForCausalLM", LSGXLMRobertaForCausalLM),
        "XLMRobertaForMultipleChoice": ("LSGXLMRobertaForMultipleChoice", LSGXLMRobertaForMultipleChoice),
        "XLMRobertaForQuestionAnswering": ("LSGXLMRobertaForQuestionAnswering", LSGXLMRobertaForQuestionAnswering),
        "XLMRobertaForSequenceClassification": ("LSGXLMRobertaForSequenceClassification", LSGXLMRobertaForSequenceClassification),
        "XLMRobertaForTokenClassification": ("LSGXLMRobertaForTokenClassification", LSGXLMRobertaForTokenClassification),
    }
    _ARCHITECTURE_TYPE_DICT = {**{"LSG" + k: v for k, v in _ARCHITECTURE_TYPE_DICT.items()}, **_ARCHITECTURE_TYPE_DICT}

    _BASE_ARCHITECTURE_TYPE = "XLMRobertaModel"
    _DEFAULT_ARCHITECTURE_TYPE = "XLMRobertaForMaskedLM"
    _CONFIG_MODULE = LSGXLMRobertaConfig

    _DEFAULT_CONFIG_POSITIONAL_OFFSET = 2
    _DEFAULT_POSITIONAL_OFFSET = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_module(self, model, is_base_architecture):
        if is_base_architecture:
            return model
        return model.roberta

    def update_global_randomly(self, module_prefix, bos_id, stride, keep_first_global):

        import torch
        from torch.distributions.multivariate_normal import MultivariateNormal

        u = module_prefix.embeddings.word_embeddings.weight.clone()
        cov = torch.cov(u.T)
        m = MultivariateNormal(u.mean(dim=0), cov)
        w = m.sample((512,))

        positions = module_prefix.embeddings.position_embeddings.weight.clone()[self._DEFAULT_POSITIONAL_OFFSET:]
        positions = self.order_positions(positions, stride)
        w[0] = u[bos_id]

        if keep_first_global:
            module_prefix.embeddings.global_embeddings.weight.data[1:] = (w + positions)[1:]
        else:
            module_prefix.embeddings.global_embeddings.weight.data = w + positions

    def update_global(self, module_prefix, bos_id, mask_id, stride, keep_first_global):

        u = module_prefix.embeddings.word_embeddings.weight.clone()
        positions = module_prefix.embeddings.position_embeddings.weight.clone()[self._DEFAULT_POSITIONAL_OFFSET:]
        positions = self.order_positions(positions, stride)
        positions[0] += u[bos_id]
        positions[1:] += u[mask_id].unsqueeze(0)

        if keep_first_global:
            module_prefix.embeddings.global_embeddings.weight.data[1:] = positions[1:]
        else:
            module_prefix.embeddings.global_embeddings.weight.data = positions
        
    def update_positions(self, module_prefix, max_pos):

        position_embeddings_weights = module_prefix.embeddings.position_embeddings.weight.clone()
        current_max_position = position_embeddings_weights.size()[0]

        new_position_embeddings_weights = torch.cat([
            position_embeddings_weights[:self._DEFAULT_POSITIONAL_OFFSET]] + 
            [position_embeddings_weights[self._DEFAULT_POSITIONAL_OFFSET:] for _ in range(max_pos//current_max_position + 1)], 
            dim=0)[:max_pos + self._DEFAULT_POSITIONAL_OFFSET]

        module_prefix.embeddings.position_embeddings = nn.Embedding(
            *new_position_embeddings_weights.size(), 
            _weight=new_position_embeddings_weights,
            dtype=new_position_embeddings_weights.dtype
            )

        self.update_buffer(module_prefix.embeddings, max_pos + self._DEFAULT_POSITIONAL_OFFSET)
        
    def update_buffer(self, module, value):
        
        # Update buffer dogshit
        module.register_buffer(
            "position_ids", torch.arange(value).expand((1, -1)), persistent=False
        )
        module.register_buffer(
            "token_type_ids", torch.zeros(module.position_ids.size(), dtype=torch.long), persistent=False
        )

    def run_test(self):
        
        from transformers import AutoConfig, AutoTokenizer

        initial_path = self.initial_model
        lsg_path = self.model_name

        config = AutoConfig.from_pretrained(lsg_path, trust_remote_code=True)
        tokenizer = AutoTokenizer.from_pretrained(lsg_path)
        text = f"Paris is the {tokenizer.mask_token} of France."

        max_length = config.max_position_embeddings - 20
        hidden_size = config.hidden_size

        self.run_models(lsg_path, max_length, hidden_size, text, AUTO_MAP)
        self.run_pipeline(lsg_path, initial_path, tokenizer, text)

    def run_pipeline(self, lsg_path, initial_path, tokenizer, text):

        from transformers import AutoModelForMaskedLM, pipeline

        model = AutoModelForMaskedLM.from_pretrained(lsg_path, trust_remote_code=True)
        pipe = pipeline("fill-mask", model=model, tokenizer=tokenizer)
        pipe_lsg = pipe(text)

        model = AutoModelForMaskedLM.from_pretrained(initial_path, trust_remote_code=True)
        pipe = pipeline("fill-mask", model=model, tokenizer=tokenizer)
        pipe_initial = pipe(text)
  
        print("\n\n" + "="*5 + " LSG PIPELINE " + "="*5 + "\n")
        print(text)
        print(pipe_lsg[0])
        print("\n\n" + "="*5 + " INITIAL PIPELINE " + "="*5 + "\n")
        print(text)
        print(pipe_initial[0])