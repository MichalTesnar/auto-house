from src.wohnen_ethz import WohnenETHZ
from src.wg_zimmer import WGZimmer

from src.personal_profile import PersonalProfile

profile = PersonalProfile("michal")

wg_zimmer = WGZimmer(profile, debug_mode=False)
wg_zimmer.search()
wg_zimmer.run()

# wohnen_ethz = WohnenETHZ(profile, debug_mode=False)
# wohnen_ethz.search()
# wohnen_ethz.run()