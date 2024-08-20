
INSTRUMENT_ARGNAME='instrument'
INSTRUMENT_ARGNAME_ALIAS='i'
TIMEFRAME_ARGNAME='timeframe'
TIMEFRAME_ARGNAME_ALIAS='t'


DATEFROM_ARGNAME='datefrom'
DATEFROM_ARGNAME_ALIAS='startdt'
DATETO_ARGNAME='dateto'
DATETO_ARGNAME_ALIAS='enddt'


NOT_FRESH_FLAG_ARGNAME = 'notfresh'
NOT_FRESH_FLAG_ARGNAME_ALIAS='old'
FRESH_FLAG_ARGNAME = 'fresh'
FRESH_FLAG_ARGNAME_ALIAS = 'new'


ARG_GROUP_INDICATOR_TITLE = 'Indicators'
ARG_GROUP_INDICATOR_DESCRIPTION = 'Indicators flags'

LARGEST_FRACTAL_PERIOD_ARGNAME="largest_fractal_period"
LARGEST_FRACTAL_PERIOD_ARGNAME_ALIAS="lfp"
LARGEST_FRACTAL_PERIOD_ARGTYPE=int

BALLIGATOR_FLAG_ARGNAME = 'balligator_flag'
BALLIGATOR_FLAG_ARGNAME_ALIAS = 'ba'
BALLIGATOR_PERIOD_JAWS_ARGNAME = "balligator_period_jaws"
BALLIGATOR_PERIOD_JAWS_ARGNAME_ALIAS = "bjaw"
BALLIGATOR_PERIOD_JAWS_ARGTYPE=int
BALLIGATOR_PERIOD_TEETH_ARGNAME="balligator_period_teeth"
BALLIGATOR_PERIOD_TEETH_ARGNAME_ALIAS="bteeth"
BALLIGATOR_PERIOD_TEETH_ARGTYPE=int
BALLIGATOR_PERIOD_LIPS_ARGNAME="balligator_period_lips"
BALLIGATOR_PERIOD_LIPS_ARGNAME_ALIAS="blips"
BALLIGATOR_PERIOD_LIPS_ARGTYPE=int


TALLIGATOR_FLAG_ARGNAME = 'talligator_flag'
TALLIGATOR_FLAG_ARGNAME_ALIAS = 'ta'
TALLIGATOR_PERIOD_JAWS_ARGNAME = "talligator_period_jaws"
TALLIGATOR_PERIOD_JAWS_ARGNAME_ALIAS = "tjaw"
TALLIGATOR_PERIOD_JAWS_ARGTYPE=int
TALLIGATOR_PERIOD_TEETH_ARGNAME="talligator_period_teeth"
TALLIGATOR_PERIOD_TEETH_ARGNAME_ALIAS="tteeth"
TALLIGATOR_PERIOD_TEETH_ARGTYPE=int
TALLIGATOR_PERIOD_LIPS_ARGNAME="talligator_period_lips"
TALLIGATOR_PERIOD_LIPS_ARGNAME_ALIAS="tlips"
TALLIGATOR_PERIOD_LIPS_ARGTYPE=int

MFI_FLAG_ARGNAME = 'mfi_flag'
NO_MFI_FLAG_ARGNAME = 'no_mfi_flag'
MFI_FLAG_ARGNAME_ALIAS = 'mfi'
NO_MFI_FLAG_ARGNAME_ALIAS = 'nomfi'

#gator_oscillator_flag,go
GATOR_OSCILLATOR_FLAG_ARGNAME = 'gator_oscillator_flag'
GATOR_OSCILLATOR_FLAG_ARGNAME_ALIAS = 'go'

#keepbidask_flag,kba
KEEP_BID_ASK_FLAG_ARGNAME = 'keepbidask'
KEEP_BID_ASK_FLAG_ARGNAME_ALIAS = 'kba'
REMOVE_BID_ASK_FLAG_ARGNAME = 'rmbidask'
REMOVE_BID_ASK_FLAG_ARGNAME_ALIAS = 'rmba'

#quotescount
QUOTES_COUNT_ARGNAME = 'quotescount'
QUOTES_COUNT_ARGNAME_ALIAS = 'c'
#full flag
FULL_FLAG_ARGNAME = 'full'
FULL_FLAG_ARGNAME_ALIAS = 'uf'
NOT_FULL_FLAG_ARGNAME = 'notfull'
NOT_FULL_FLAG_ARGNAME_ALIAS = 'nf'

#dropna_volume
DROPNA_VOLUME_FLAG_ARGNAME = 'dropna_volume'
DROPNA_VOLUME_FLAG_ARGNAME_ALIAS = 'dv'
#dont_dropna_volume
DONT_DROPNA_VOLUME_FLAG_ARGNAME = 'dont_dropna_volume'
DONT_DROPNA_VOLUME_FLAG_ARGNAME_ALIAS = 'ddv'

ARG_GROUP_POV_TITLE="POV"
ARG_GROUP_POV_DESCRIPTION="Point of view"
ARG_GROUP_RANGE_TITLE="DTRange"
ARG_GROUP_RANGE_DESCRIPTION="Date and range selection"


ARG_GROUP_BARS_TITLE="Bars"
ARG_GROUP_BARS_DESCRIPTION="Bars flags"

ARG_GROUP_CLEANUP_TITLE = 'Cleanup'
ARG_GROUP_CLEANUP_DESCRIPTION = 'Cleanup data'

ARG_GROUP_VERBOSITY_TITLE="Verbosity"
ARG_GROUP_VERBOSITY_DESCRIPTION="control the verbosity of the output"

ARG_GROUP_OUTPUT_TITLE="Output"
ARG_GROUP_OUTPUT_DESCRIPTION="Output arguments"

OUTPUT_ARGNAME = 'output'
OUTPUT_ARGNAME_ALIAS = 'o'

MD_FLAG_ARGNAME = "markdown_output"
MD_FLAG_ARGNAME_ALIAS = "md"
JSON_FLAG_ARGNAME = "json_output"
JSON_FLAG_ARGNAME_ALIAS = "json"

ARG_GROUP_INTERACTION_TITLE="Interaction"
ARG_GROUP_INTERACTION_DESCRIPTION="Interaction arguments"


TLID_RANGE_ARGNAME='range'
TLID_RANGE_ARG_DEST='tlidrange'
TLID_RANGE_ARGNAME_ALIAS='tlid'
TLID_RANGE_HELP_STRING='TLID range are two dates formated: YYMMDDHHMM_YYMMDDHHMM.'



DEMO_FLAG_ARGNAME='demo'
REAL_FLAG_ARGNAME='real'

SETTING_ARGNAME='settings'
SETTING_ARGNAME_ALIAS='ls'


RATE_ARGNAME='rate'
RATE_ARGNAME_ALIAS='r'

BUYSELL_ARGNAME='bs'
BUYSELL_ARGNAME_ALIAS='d'

STOP_ARGNAME='stop'
STOP_ARGNAME_ALIAS='x' 

PIPS_ARGNAME='pips'

LOTS_ARGNAME='lots'
LOTS_ARGNAME_ALIAS='n'

ORDERID_ARGNAME='orderid'
ORDERID_ARGNAME_ALIAS='id'

TRADEID_ARGNAME='tradeid'
TRADEID_ARGNAME_ALIAS='tid'

ACCOUNT_ARGNAME='account'

PN_GROUP_NAME = "Patterns"
PN_ARGNAME = "patternname"
PN_ARGNAME_ALIAS = "pn"
PN_COLUMN_LIST_ARGNAME = "columns_list_from_higher_tf"
PN_COLUMN_LIST_ARGNAME_ALIAS = "clh"
PN_LIST_FLAG_ARGNAME = "list_patterns"
PN_LIST_FLAG_ARGNAME_ALIAS = "pls"

SELECTED_COLUMNS_GROUP_NAME = "Selected Columns"
SELECTED_COLUMNS_ARGNAME = "selected_columns"
SELECTED_COLUMNS_ARGNAME_ALIAS = "sc"
SELECTED_COLUMNS_HELP = "List of columns to get from higher TF.  Default is mfi_sig,zone_sig,ao"


PDSCLI_PROG_NAME='jgtfxcli'
CLI_FXRMORDER_PROG_NAME='fxrmorder'
CLI_FXADDORDER_PROG_NAME='fxaddorder'
CLI_FXTR_PROG_NAME='fxtr'
CLI_FXRMTRADE_PROG_NAME='fxrmtrade'
CLI_FXMVSTOP_PROG_NAME='fxmvstop'

JGT_SUBDIR_NAME = ".jgt"
JGT_ENV_EXPORT_NAME=".env.jgtset"
JGT_FXTRADE_ENV_FILENAME='.env.fxtrade'

JGTSET_CLI_EPILOG = "Load,output and/or export settings as JSON/YML or environment variables in "+JGT_SUBDIR_NAME+"/"+JGT_ENV_EXPORT_NAME

JGTSET_CLI_DESCRIPTION = "JGTFxCLI Settings Loader"
JGTSET_CLI_PROG_NAME="jgtset"
_JGTSET_EXCLUDED_ENV_EXPORT_KEYS=['QM_HISTORY_PATH']

JGT_DATA_DIR="data"
JGT_DATA_SUBDIRDIR="jgt"
JGT_FXDATA_NS="fx"

#@STCIssue Defined in jgtpy for now
# IDSCLI_PROG_NAME='idscli'
# JGTADS_PROG_NAME='jgtads'
# JGTCLI_PROG_NAME='jgtcli'
# JGTMKS_PROG_NAME='jgtmks'
