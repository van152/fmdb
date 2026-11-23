char __fastcall sub_140EB6500(__int64 a1, int a2, __int64 *a3)
{
  char result; // al
  char v6; // cl
  __int64 v7; // rbx
  __int64 v8; // rbx
  unsigned int v9; // eax
  int v10; // [rsp+28h] [rbp-30h] BYREF
  __int64 v11[5]; // [rsp+30h] [rbp-28h] BYREF

  result = 0;
  switch ( a2 )
  {
    case 1447121508:
LABEL_5:
      if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B5C8D0);
        if ( dword_141B5C8D0 == -1 )
        {
          sub_140DBC9B0(&qword_141B5C8A0);
          sub_141751048(sub_140DBCA10);
          sub_141750EA0(&dword_141B5C8D0);
        }
      }
      if ( (__int64 *)*a3 == &qword_141B5C8A0 )
      {
        v9 = *((_DWORD *)a3 + 2);
        HIWORD(v10) = v9 >> 17;
        LOWORD(v10) = (v9 >> 8) & 0x1FF | ((_WORD)v9 << 9);
      }
      else if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
      {
        (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)*a3 + 160LL))(*a3, v11, a3);
        sub_1413CA830(&v10, v11);
      }
      else
      {
        v10 = 124518401;
      }
      *(_DWORD *)(a1 + 16) = v10;
      goto LABEL_18;
    case 1447121509:
    case 1447121511:
    case 1447121512:
    case 1447121513:
    case 1447121514:
    case 1447121515:
    case 1447121516:
    case 1447121518:
    case 1447121519:
    case 1447121520:
    case 1447121521:
    case 1447121522:
    case 1447121525:
      return result;
    case 1447121510:
      v6 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
      *(_BYTE *)(a1 + 22) = v6;
      result = 1;
      if ( v6 != 0 )
      {
        *(_QWORD *)(a1 + 8) = 0;
        *(_QWORD *)a1 = 0;
      }
      return result;
    case 1447121517:
LABEL_9:
      v7 = qword_141B5FE38;
      sub_140FE7960((__int64)v11, a3, 0x7374676Eu);
      *(_QWORD *)a1 = sub_140FA3700(v7, (int *)v11);
      goto LABEL_18;
    case 1447121523:
LABEL_10:
      v8 = qword_141B5FE38;
      sub_140FE7960((__int64)v11, a3, 0x7374676Eu);
      *(_QWORD *)(a1 + 8) = sub_140FA3700(v8, (int *)v11);
      goto LABEL_18;
    case 1447121524:
      *(_BYTE *)(a1 + 20) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      goto LABEL_18;
    case 1447121526:
LABEL_11:
      *(_BYTE *)(a1 + 21) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
LABEL_18:
      result = 1;
      break;
    default:
      switch ( a2 )
      {
        case 1212892516:
          goto LABEL_5;
        case 1212892525:
          goto LABEL_9;
        case 1212892531:
          goto LABEL_10;
        case 1212892532:
          if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 48LL))(*a3, a3) != 0 )
            *(_BYTE *)(a1 + 20) = 100;
          else
            *(_BYTE *)(a1 + 20) = 5;
          goto LABEL_18;
        case 1212892534:
          goto LABEL_11;
        default:
          return result;
      }
  }
  return result;
}
