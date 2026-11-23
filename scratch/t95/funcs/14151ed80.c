char __fastcall sub_14151ED80(_BYTE *a1, int a2, _QWORD *a3)
{
  char result; // al

  result = 0;
  switch ( a2 )
  {
    case 1130591074:
LABEL_3:
      a1[4] = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      goto LABEL_10;
    case 1130591075:
    case 1130591076:
    case 1130591077:
    case 1130591079:
    case 1130591081:
    case 1130591082:
    case 1130591084:
    case 1130591085:
    case 1130591086:
    case 1130591087:
    case 1130591089:
    case 1130591091:
    case 1130591092:
    case 1130591093:
    case 1130591094:
    case 1130591095:
    case 1130591096:
      return result;
    case 1130591078:
LABEL_4:
      a1[2] = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      goto LABEL_10;
    case 1130591080:
LABEL_5:
      a1[5] = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      goto LABEL_10;
    case 1130591083:
LABEL_6:
      a1[1] = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      goto LABEL_10;
    case 1130591088:
LABEL_7:
      *a1 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      goto LABEL_10;
    case 1130591090:
LABEL_8:
      a1[3] = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      goto LABEL_10;
    case 1130591097:
LABEL_9:
      a1[6] = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
LABEL_10:
      result = 1;
      break;
    default:
      switch ( a2 )
      {
        case 1348694882:
          goto LABEL_3;
        case 1348694886:
          goto LABEL_4;
        case 1348694888:
          goto LABEL_5;
        case 1348694891:
          goto LABEL_6;
        case 1348694896:
          goto LABEL_7;
        case 1348694898:
          goto LABEL_8;
        case 1348694905:
          goto LABEL_9;
        default:
          return result;
      }
  }
  return result;
}
