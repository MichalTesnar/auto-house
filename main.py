from src.wohnen_ethz import WohnenETHZ
from src.wg_zimmer import WGZimmer

from src.personal_profile import PersonalProfile

profile = PersonalProfile("example_name")

# wg_zimmer = WGZimmer(profile, debug_mode=True)
# wg_zimmer.search()
# wg_zimmer.run()

wohnen_ethz = WohnenETHZ(profile, debug_mode=True)
wohnen_ethz.search()
wohnen_ethz.run()