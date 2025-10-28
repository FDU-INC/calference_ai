# Copyright (C) 2025 FDU-INC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info

class LLMInference:
    def __init__(self, model_path):
        """初始化LLM推理类"""
        print("正在加载模型，请稍候...")
        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            model_path, torch_dtype="auto", device_map="auto"
        )
        self.processor = AutoProcessor.from_pretrained(model_path)
        print("模型加载完成。")

    def generate_analysis(self, image_or_messages, prompt=None):
        """
        支持两种调用方式：
        1. 单图+prompt：image_or_messages为图片路径（str），prompt为文本
        2. Qwen多模态：image_or_messages为messages（list/dict），prompt为None
        """
        if prompt is not None:
            # 单图+prompt
            messages = [{"role": "user", "content": [{"type": "image", "image": image_or_messages}, {"type": "text", "text": prompt}]}]
        else:
            # 多模态messages
            messages = image_or_messages
        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt",
            )
        inputs = inputs.to("cuda")
        print(f"正在生成分析报告...")
        generated_ids = self.model.generate(**inputs, max_new_tokens=4096)
        generated_ids_trimmed = [out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
        output_text = self.processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)
        return output_text[0]
