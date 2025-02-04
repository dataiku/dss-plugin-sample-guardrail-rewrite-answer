from dataiku.llm.guardrails import BaseGuardrail
import requests
import dataiku

class WhimsicalGuardrail(BaseGuardrail):
    def set_config(self, config, plugin_config):
        self.config = config

    def process(self, input, trace):
        if "completionResponse" in input:
            text_to_rewrite = input["completionResponse"]["text"]
            
            with trace.subspan("Rewriting whimsically") as subspan:
            
                llm = dataiku.api_client().get_default_project().get_llm(self.config["llm"])
                c = llm.new_completion() \
                    .with_message("Please rewrite the following text, in a more whimsical way", "system") \
                    .with_message(text_to_rewrite)
                r = c.execute()
            
                input["completionResponse"]["text"] = r.text
                
                subspan.append_trace(r.trace)
         
        return input