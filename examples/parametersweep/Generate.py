import c302
from c302.c302_IClampMuscle import setup

setup('C0',
      generate=True,
      target_directory='./',
      param_overrides={"unphysiological_offset_current":'1pA'})


