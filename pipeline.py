# pipeline.py

import re
import time

from agents import writer_chain, critic_chain
from tools import search_tool, scrape_tool


def run_research_pipeline(topic: str):

    state = {}

    # ==================================================
    # STEP 1 : SEARCH
    # ==================================================

    print("\n" + "=" * 50)
    print("STEP 1 - Searching the web...")
    print("=" * 50)

    search_result = search_tool.invoke(
        f"Find recent, reliable and detailed information about: {topic}"
    )

    state["search_results"] = str(search_result)

    print("\nSEARCH RESULTS:\n")
    print(state["search_results"][:2000])

    # ==================================================
    # STEP 2 : FIND URL
    # ==================================================

    print("\n" + "=" * 50)
    print("STEP 2 - Finding URLs...")
    print("=" * 50)

    urls = re.findall(
        r'https?://[^\s\',]+',
        state["search_results"]
    )

    if not urls:

        print("\nNo URLs found!")

        state["scraped_content"] = "No URL found."

    else:

        best_url = urls[0]

        print(f"\nSelected URL:\n{best_url}")

        # ==================================================
        # STEP 3 : SCRAPE CONTENT
        # ==================================================

        print("\n" + "=" * 50)
        print("STEP 3 - Scraping webpage...")
        print("=" * 50)

        try:

            scraped_result = scrape_tool.invoke(
                {
                    "url": best_url
                }
            )

            try:

                # Hyperbrowser response
                state["scraped_content"] = (
                    str(scraped_result["data"].markdown)
                )[:3000]

            except:

                state["scraped_content"] = (
                    str(scraped_result)
                )[:3000]

        except Exception as e:

            state["scraped_content"] = (
                f"Scraping failed: {str(e)}"
            )

    print("\nSCRAPED CONTENT:\n")
    print(state["scraped_content"])

    # ==================================================
    # STEP 4 : WRITER
    # ==================================================

    print("\n" + "=" * 50)
    print("STEP 4 - Writing research report...")
    print("=" * 50)

    research_combined = f"""
SEARCH RESULTS:
{state['search_results']}

SCRAPED CONTENT:
{state['scraped_content']}
"""

    try:

        state["report"] = writer_chain.invoke(
            {
                "topic": topic,
                "research": research_combined
            }
        )

    except Exception as e:

        print(f"\nWriter Error: {e}")
        return state

    print("\nFINAL REPORT:\n")
    print(state["report"])

    # ==================================================
    # STEP 5 : CRITIC
    # ==================================================

    print("\n" + "=" * 50)
    print("STEP 5 - Reviewing report...")
    print("=" * 50)

    try:

        print("\nWaiting 10 seconds before critic...")
        time.sleep(10)

        state["feedback"] = critic_chain.invoke(
            {
                "report": state["report"]
            }
        )

        print("\nCRITIC FEEDBACK:\n")
        print(state["feedback"])

    except Exception as e:

        state["feedback"] = (
            f"Critic could not run due to API error:\n{str(e)}"
        )

        print("\nCRITIC ERROR:\n")
        print(state["feedback"])

    return state


if __name__ == "__main__":

    topic = input("\nEnter a research topic: ")

    run_research_pipeline(topic)