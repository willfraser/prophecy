import quadrigacx
import polling

polling.poll(
lambda: print(quadrigacx.get_current_trades("ltc_cad")['last']),
step=10,
poll_forever=True)

