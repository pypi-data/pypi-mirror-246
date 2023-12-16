"""Functions related to ratings."""


from optimal_congress.config import DIR_RATINGS_CACHE
from optimal_congress.models import Event, Rating


def filter_latest_ratings(ratings: set[Rating]) -> set[Rating]:
    """Return the latest rating for each event.

    Args:
        ratings: List of ratings.
    Returns:
        List of latest ratings.
    """
    # sort ratings by timestamp, descending
    ratings_sorted = sorted(
        list(ratings), key=lambda rating: rating.timestamp, reverse=True
    )

    # keep only latest rating for each event
    latest_ratings: set[Rating] = set()
    for rating in ratings_sorted:
        if rating.event_id not in [r.event_id for r in latest_ratings]:
            latest_ratings.add(rating)
    return latest_ratings


def filter_unrated_events(
    events: set[Event],
    ratings: set[Rating],
) -> set[Event]:
    """Return the unrated events from a list of events based on previous ratings.

    Args:
        events: list of events.
        previous_ratings: list of previous ratings.
    Returns:
        List of events for which no rating is provided.
    """
    rated_event_ids = {rating.event_id for rating in ratings}
    unrated_events = {event for event in events if event.id not in rated_event_ids}
    return unrated_events


def enquire_and_save_ratings(events: set[Event]) -> None:
    """Enquire and save ratings for a list of events."""

    for i, event in enumerate(events):
        print(f"\nEvent ({i + 1}/{len(events)}):\n  {event}")
        try:
            score = input("Rate from 0 to 10 (Enter to exit): ")
            if score == "":
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            print("\nExiting.")
            break

        rating = Rating(event_id=event.id, score=float(score))

        # save rating
        with open(DIR_RATINGS_CACHE / f"rating_{event.id}.json", "w") as f:
            print(f"Saving rating '{rating.score}' for event '{event.name}'...")
            f.write(rating.model_dump_json())
