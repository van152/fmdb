char __fastcall sub_143FCA160(__int64 a1, int a2, _QWORD *a3)
{
  char result; // al
  char v6; // al
  char v7; // cl
  __int64 v8; // rbx
  char v9; // al
  char v10; // cl
  char v11; // cl
  __int64 v12; // rbx
  __int64 v13; // rbx
  char v14; // al
  char v15; // cl
  _BYTE v16[40]; // [rsp+20h] [rbp-28h] BYREF

  result = 0;
  if ( a2 <= 1416456300 )
  {
    if ( a2 <= 1131247712 )
    {
      if ( a2 == 1130460260 )
      {
        *(_DWORD *)(a1 + 56) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      }
      else
      {
        if ( a2 != 1131245153 )
          return result;
        *(_DWORD *)(a1 + 64) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      }
    }
    else
    {
      switch ( a2 )
      {
        case 1131247713:
          *(_DWORD *)(a1 + 60) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          break;
        case 1415870057:
          v13 = qword_141B5FDC0;
          sub_140FE7960(v16, a3, 1668246896);
          *(_QWORD *)(a1 + 32) = sub_140F7A940(v13, v16);
          break;
        case 1416389737:
          v8 = qword_141B5FDC0;
          sub_140FE7960(v16, a3, 1668246896);
          *(_QWORD *)(a1 + 40) = sub_140F7A940(v8, v16);
          break;
        default:
          return result;
      }
    }
  }
  else if ( a2 > 1417111660 )
  {
    if ( a2 == 1417111661 )
    {
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
        *(_BYTE *)(a1 + 69) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      else
        *(_BYTE *)(a1 + 69) = 0;
    }
    else
    {
      if ( a2 == 1953328751 )
      {
        v14 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
        v15 = *(_BYTE *)(a1 + 71);
        if ( v14 != 0 )
          v11 = v15 | 4;
        else
          v11 = v15 & 0xFB;
      }
      else
      {
        if ( a2 != 1953328758 )
          return result;
        v9 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
        v10 = *(_BYTE *)(a1 + 71);
        if ( v9 != 0 )
          v11 = v10 | 2;
        else
          v11 = v10 & 0xFD;
      }
      *(_BYTE *)(a1 + 71) = v11;
    }
  }
  else
  {
    switch ( a2 )
    {
      case 1416456301:
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
          *(_BYTE *)(a1 + 70) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        else
          *(_BYTE *)(a1 + 70) = 0;
        break;
      case 1416852585:
        v12 = qword_141B5FE28;
        sub_140FE7960(v16, a3, 1937006948);
        *(_QWORD *)(a1 + 48) = sub_140F7A940(v12, v16);
        break;
      case 1416919408:
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
        {
          v6 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          v7 = 1;
          if ( v6 != -1 )
            v7 = v6;
          *(_BYTE *)(a1 + 68) = v7;
        }
        else
        {
          *(_BYTE *)(a1 + 68) = -1;
        }
        break;
      default:
        return result;
    }
  }
  return 1;
}
