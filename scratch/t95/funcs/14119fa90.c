char __fastcall sub_14119FA90(__int64 a1, int a2, _QWORD *a3)
{
  char result; // al
  __int64 v6; // rbx
  _BYTE v7[40]; // [rsp+20h] [rbp-28h] BYREF

  result = 0;
  if ( a2 > 1869767780 )
  {
    if ( a2 > 1886352232 )
    {
      switch ( a2 )
      {
        case 1886352233:
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
            *(_BYTE *)(a1 + 57) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          else
            *(_BYTE *)(a1 + 57) = -1;
          break;
        case 2003398259:
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
            *(_BYTE *)(a1 + 59) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          else
            *(_BYTE *)(a1 + 59) = -1;
          break;
        case 2036687218:
          *(_WORD *)(a1 + 54) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 80LL))(*a3, a3);
          break;
        default:
          return result;
      }
    }
    else
    {
      switch ( a2 )
      {
        case 1869767781:
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
            *(_BYTE *)(a1 + 56) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          else
            *(_BYTE *)(a1 + 56) = 0;
          break;
        case 1886151033:
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
            *(_BYTE *)(a1 + 58) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          else
            *(_BYTE *)(a1 + 58) = -1;
          break;
        case 1886349678:
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
            *(_WORD *)(a1 + 52) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          else
            *(_WORD *)(a1 + 52) = -1;
          break;
        default:
          return result;
      }
    }
  }
  else if ( a2 > 1734766449 )
  {
    switch ( a2 )
    {
      case 1734766450:
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
          *(_WORD *)(a1 + 48) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        else
          *(_WORD *)(a1 + 48) = -1;
        break;
      case 1819243380:
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
          *(_BYTE *)(a1 + 61) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        else
          *(_BYTE *)(a1 + 61) = -1;
        break;
      case 1836610669:
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
          *(_BYTE *)(a1 + 62) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        else
          *(_BYTE *)(a1 + 62) = -1;
        break;
      default:
        return result;
    }
  }
  else
  {
    switch ( a2 )
    {
      case 1684633193:
        v6 = qword_141B5FDC0;
        sub_140FE7960(v7, a3, 1668246896);
        *(_QWORD *)(a1 + 24) = sub_140F7A940(v6, v7);
        break;
      case 1685217655:
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
          *(_BYTE *)(a1 + 60) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        else
          *(_BYTE *)(a1 + 60) = -1;
        break;
      case 1734436705:
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
          *(_WORD *)(a1 + 50) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        else
          *(_WORD *)(a1 + 50) = -1;
        break;
      default:
        return result;
    }
  }
  return 1;
}
