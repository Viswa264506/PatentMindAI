from typing import List, Dict
import time
import requests

from backend.schemas.state import Patent
from backend.config.settings import settings, logger


class PatentSearchTool:

    BASE_URL = "https://api.patentsview.org/patents/query"

    def search_patentsview(self, queries: List[str]) -> List[Patent]:
        """
        Search PatentsView using multiple semantic search queries.
        Returns top 20 unique patents.
        """

        logger.info(f"Searching PatentsView using {len(queries)} queries")

        all_results: Dict[str, Patent] = {}

        for query in queries:

            payload = {
                "q": {
                    "_text_any": {
                        "patent_abstract": query
                    }
                },
                "f": [
                    "patent_number",
                    "patent_title",
                    "patent_abstract"
                ],
                "o": {
                    "per_page": 10
                }
            }

            retries = 3

            for attempt in range(retries):

                try:

                    response = requests.post(
                        self.BASE_URL,
                        json=payload,
                        timeout=getattr(settings, "REQUEST_TIMEOUT", 10)
                    )

                    response.raise_for_status()

                    data = response.json()

                    patents = data.get("patents", [])

                    logger.info(
                        f"Query '{query}' returned {len(patents)} patents."
                    )

                    for p in patents:

                        patent_number = p.get("patent_number")

                        if not patent_number:
                            continue

                        if patent_number not in all_results:

                            all_results[patent_number] = Patent(
                                patent_number=patent_number,
                                title=p.get("patent_title", "Untitled"),
                                abstract=p.get(
                                    "patent_abstract",
                                    "No abstract available"
                                ),
                                provider="PatentsView",

                                # Remove this field if it
                                # doesn't exist in your schema
                            )

                    break

                except Exception as e:

                    logger.error(f"Error: {e}")

                    if 'response' in locals():
                        print("\n" + "=" * 80)
                        print("STATUS :", response.status_code)
                        print("=" * 80)
                        print(response.text[:1000])
                        print("=" * 80)

                    if attempt < retries - 1:
                        time.sleep(1)
                    else:
                        logger.error(
                            f"Failed searching query '{query}' after {retries} attempts."
                        )

        logger.info(
            f"Total unique patents collected: {len(all_results)}"
        )

        return list(all_results.values())[:20]

    def search_uspto(self, query: str) -> List[Patent]:
        """
        Placeholder for USPTO integration.
        """

        logger.info(f"USPTO search requested: {query}")

        if not settings.USPTO_API_KEY:
            logger.warning(
                "USPTO API key not configured."
            )
            return []

        # TODO:
        # Implement USPTO API here

        return []