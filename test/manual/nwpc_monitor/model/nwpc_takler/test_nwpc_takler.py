from nwpc_monitor.model.nwpc_takler.commit import Commit
import time

c = Commit()

c.id = '1'
c.owner = 'wangdp'
c.repo = 'wangdp-repo'
c.timestamp = time.time()

c.set_data({
    'committer': 'nwp_xp',
    'type': 'status'
})

print(c.to_dict())