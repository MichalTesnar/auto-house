from src.wohnen_ethz import WohnenETHZ
from src.wg_zimmer import WGZimmer
from src.flatfox import Flatfox

from src.personal_profile import PersonalProfile

profile = PersonalProfile("michal")

# wg_zimmer = WGZimmer(profile, confirmation_mode=True)
# wg_zimmer.search()
# wg_zimmer.run()

# wohnen_ethz = WohnenETHZ(profile)
# wohnen_ethz.search()
# wohnen_ethz.run()

flatfox = Flatfox(profile, confirmation_mode=True)
flatfox.search()
flatfox.run()