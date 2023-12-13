try:
	from zrcl3.desktop_automation import (
		capture_window, 
		find_word_coordinates, 
	)
except ImportError:
	capture_window = None
	find_word_coordinates = None

try:
	from zrcl3.expirable_property import (
		TimelyCachedProperty, 
		time_sensitive_cache, 
	)
except ImportError:
	TimelyCachedProperty = None
	time_sensitive_cache = None

try:
	from zrcl3.github_download import (
		download_github_repo_file, 
	)
except ImportError:
	download_github_repo_file = None

try:
	from zrcl3.init_generator import (
		gather_init_vars, 
		generate_init, 
	)
except ImportError:
	gather_init_vars = None
	generate_init = None

try:
	from zrcl3.io import (
		create_bkup, 
	)
except ImportError:
	create_bkup = None

try:
	from zrcl3.list_module import (
		get_imports, 
		get_imports_via_ast, 
	)
except ImportError:
	get_imports = None
	get_imports_via_ast = None

try:
	from zrcl3.orjson_io_fallback import (
		load_json, 
		save_json, 
	)
except ImportError:
	load_json = None
	save_json = None

try:
	from zrcl3.singleton import (
		SingletonMeta, 
	)
except ImportError:
	SingletonMeta = None

try:
	from zrcl3.subprocess import (
		is_program_installed, 
	)
except ImportError:
	is_program_installed = None

try:
	from zrcl3.verify_file import (
		checksum_verify, 
		is_size_within_range, 
	)
except ImportError:
	checksum_verify = None
	is_size_within_range = None

try:
	from zrcl3.win_process import (
		get_pid_from_hwnd, 
	)
except ImportError:
	get_pid_from_hwnd = None

try:
	from zrcl3.auto_click.ctx import (
		AutoClickCtx, 
		AutoClickMarker, 
	)
except ImportError:
	AutoClickCtx = None
	AutoClickMarker = None

try:
	from zrcl3.auto_click import (
		create_click_command, 
		create_click_file, 
		create_click_folder, 
		create_click_module, 
	)
except ImportError:
	create_click_command = None
	create_click_file = None
	create_click_folder = None
	create_click_module = None

try:
	from zrcl3.auto_save_dict.on_trigger import (
		OnChangeSaveDict, 
	)
except ImportError:
	OnChangeSaveDict = None

try:
	from zrcl3.auto_save_dict.threaded import (
		AutoSaveDict, 
	)
except ImportError:
	AutoSaveDict = None

