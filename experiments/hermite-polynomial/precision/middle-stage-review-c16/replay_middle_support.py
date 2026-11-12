"""Read-only import of reviewed replay helpers despite hyphenated filename."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('middle_full_replay',Path(__file__).with_name('replay-middle.py'))
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
HERE,ROOT,REL,sha,sanitize=module.HERE,module.ROOT,module.REL,module.sha,module.sanitize
