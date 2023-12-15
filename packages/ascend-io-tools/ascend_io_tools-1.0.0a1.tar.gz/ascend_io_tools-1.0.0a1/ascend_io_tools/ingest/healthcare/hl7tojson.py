import logging as log

from hl7 import parse
from hl7.containers import Repetition


def parse_hl7(hl7_input: str) -> {}:
  output = {}
  h = parse(hl7_input)

  seg_idx = field_idx = 0
  try:
    for seg_idx in range(0, len(h)):
      seg = h[seg_idx]
      seg_name = seg[0]
      seg_num = seg[1]
      seg_key = f'{seg_name}-{seg_num[0]}' if seg_idx and seg_num[0] else f'{seg_name}'
      log.debug(f'Parsing segment {seg_key}')
      seg_obj = {}
      output[seg_key] = seg_obj
      # message header fields have a special separator
      if seg_idx == 0:
        seg_obj[f'{seg_name}.1'] = seg_num[0]
      for field_idx in range(2, len(seg)):
        field = seg[field_idx]
        if isinstance(field[0], Repetition):
          rep = field[0]
          rep_obj = {}
          seg_obj[f'{seg_key}.{field_idx}'] = rep_obj
          for rep_idx in range(0, len(rep)):
            rep_val = rep[rep_idx]
            rep_key = f'{seg_key}.{field_idx}.{rep_idx + 1}'
            if isinstance(rep_val[0], str):
              rep_obj[rep_key] = rep_val[0]
            else:
              log.debug(f'HL7 value was {type(rep_val[0])} instead of a string')
              rep_obj[rep_key] = rep_val
        else:
          field_key = f'{seg_key}.{field_idx}'
          seg_obj[field_key] = field[0]
  except Exception as ex:
    raise Exception(f'Parse failed for segment: {seg_idx}, field {field_idx}') from ex
  return output
