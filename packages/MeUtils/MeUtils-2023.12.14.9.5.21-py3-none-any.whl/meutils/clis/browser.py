#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : browser
# @Time         : 2023/11/29 15:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from playwright.async_api import Playwright, async_playwright

cli = typer.Typer(name="模拟浏览器")


async def playwright_run(
        url: str = "https://kimi.moonshot.cn/",
        headless: bool = False,
        storage_state: str = 'kimi_*.json',
        timeout: int = 1000

):
    storages = []
    for storage_state in Path().rglob(storage_state):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=headless)
            context = await browser.new_context(storage_state=storage_state if Path(storage_state).exists() else None)

            page = await context.new_page()

            await page.goto(url)
            await page.wait_for_load_state(state='load')
            await page.wait_for_load_state(state='networkidle')
            await page.wait_for_load_state(state='domcontentloaded')
            await page.wait_for_timeout(timeout=timeout)

            # ---------------------
            # 保存状态文件
            storage = await context.storage_state(path=storage_state)
            storages.append(storage)
            await context.close()
            await browser.close()
    return storages


@cli.command()
def prun(
        url: str = "https://kimi.moonshot.cn/",
        headless: bool = True,
        storage_state: str = 'state.json'
):
    """
    mecli-browser --no-headless --url  https://kimi.moonshot.cn/
    """
    storage = asyncio.run(playwright_run(url, headless, storage_state))
    logger.debug(storage)


if __name__ == '__main__':
    cli()
