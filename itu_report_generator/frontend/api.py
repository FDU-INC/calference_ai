# GNU GENERAL PUBLIC LICENSE
# Version 3, 29 June 2007
#
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
#
# Author: yjh
# Date: 2026-02-07
import os
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from report_service import generate_report
from config import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_MODEL_NAME,
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = DATA_DIR / "output_reports"
UPLOAD_DIR = DATA_DIR / "uploaded"
SAMPLE_DIR = DATA_DIR / "total"
STATIC_DIR = Path(__file__).resolve().parent / "static"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Interference Report Frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/data", StaticFiles(directory=DATA_DIR), name="data")


def _list_images(folder: Path) -> List[Dict]:
    if not folder.exists():
        return []
    return [
        {
            "name": p.name,
            "path": str(p.relative_to(BASE_DIR)),
            "size": p.stat().st_size,
        }
        for p in sorted(folder.glob("*.png"))
    ]


@app.get("/")
async def index():
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_file)


@app.get("/api/images")
async def list_images():
    return {
        "samples": _list_images(SAMPLE_DIR),
        "uploaded": _list_images(UPLOAD_DIR),
    }


@app.post("/api/generate")
async def generate(
    image_option: str = Form("sample"),
    image_path: Optional[str] = Form(None),
    use_rag: bool = Form(True),
    model_name: Optional[str] = Form(None),
    base_url: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None),
    file: UploadFile = File(None),
):
    try:
        # 统一解析 LLM 配置：表单参数 > 环境变量 > config.py 默认值
        resolved_api_key = (
            api_key
            or os.getenv("LLM_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or LLM_API_KEY
        )
        resolved_base_url = base_url or os.getenv("LLM_BASE_URL", LLM_BASE_URL)
        resolved_model = model_name or os.getenv("LLM_MODEL_NAME", LLM_MODEL_NAME)

        if not resolved_api_key:
            raise HTTPException(status_code=400, detail="缺少 API Key，请在环境变量或表单中提供")

        # 解析图片输入：支持 sample / upload 两种模式
        if image_option == "upload":
            if file is None:
                raise HTTPException(status_code=400, detail="请上传图片文件")
            dest = UPLOAD_DIR / file.filename
            dest.write_bytes(await file.read())
            target_path = dest
        else:
            if not image_path:
                raise HTTPException(status_code=400, detail="请提供图片路径")
            target_path = (BASE_DIR / image_path).resolve()
            if not target_path.exists():
                raise HTTPException(
                    status_code=404, detail=f"图片未找到: {target_path}"
                )

        result = await generate_report(
            image_path=target_path,
            use_rag=use_rag,
            model_name=resolved_model,
            base_url=resolved_base_url,
            api_key=resolved_api_key,
            output_dir=OUTPUT_DIR,
        )

        md_rel = Path(result["markdown_path"]).resolve().relative_to(BASE_DIR)
        docx_rel = (
            Path(result["docx_path"]).resolve().relative_to(BASE_DIR)
            if result.get("docx_path")
            else None
        )
        image_rel = Path(result["image_path"]).resolve().relative_to(BASE_DIR)

        return {
            "status": "ok",
            "markdown": result["markdown"],
            "markdown_path": str(md_rel),
            "docx_path": str(docx_rel) if docx_rel else None,
            "image_path": str(image_rel),
            "rag_results": result.get("rag_results", []),
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback

        print("[/api/generate] error:", type(e).__name__, str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health():
    return {"status": "healthy"}


