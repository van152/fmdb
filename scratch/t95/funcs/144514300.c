char __fastcall sub_144514300(__int64 a1, int a2, _QWORD *a3)
{
  char result; // al
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rax
  char v12; // cl
  _BYTE v13[40]; // [rsp+20h] [rbp-28h] BYREF

  result = 0;
  if ( a2 <= 1886352232 )
  {
    if ( a2 > 1701083505 )
    {
      if ( a2 == 1701083506 )
      {
        *(_WORD *)(a1 + 74) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 80LL))(*a3, a3);
      }
      else
      {
        if ( a2 != 1836282990 )
          return result;
        v8 = qword_141B5FE38;
        sub_140FE7960(v13, a3, 1937008494);
        *(_QWORD *)(a1 + 48) = sub_140FA3700(v8, v13);
      }
    }
    else if ( a2 == 1668380006 )
    {
      v10 = qword_141B5FDC0;
      sub_140FE7960(v13, a3, 1668246896);
      *(_QWORD *)(a1 + 40) = sub_140F7A940(v10, v13);
    }
    else
    {
      if ( a2 != 1684173428 )
        return result;
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *, __int64 *))(*(_QWORD *)*a3
                                                                          + 8LL * (*a3 != qword_141B5A4A0)
                                                                          + 32))(
             *a3,
             a3,
             &qword_141B5A4A0) != 0 )
      {
        *(_WORD *)(a1 + 76) = 0;
      }
      else
      {
        v11 = (*(char (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3) - 1LL;
        v12 = -1;
        if ( (unsigned int)v11 <= 0x12 )
        {
          v12 = *(_BYTE *)(v11 + 0x1418BE7EFLL);
          *(_BYTE *)(a1 + 76) = *(_BYTE *)(v11 + 0x1418BE7DCLL);
        }
        *(_BYTE *)(a1 + 77) = v12;
      }
    }
  }
  else if ( a2 <= 1937013105 )
  {
    if ( a2 == 1886352233 )
    {
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
        *(_BYTE *)(a1 + 78) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      else
        *(_BYTE *)(a1 + 78) = -1;
    }
    else
    {
      if ( a2 != 1936946286 )
        return result;
      v7 = qword_141B5FE38;
      sub_140FE7960(v13, a3, 1937008494);
      *(_QWORD *)(a1 + 56) = sub_140FA3700(v7, v13);
    }
  }
  else
  {
    switch ( a2 )
    {
      case 1937013106:
        *(_WORD *)(a1 + 72) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 80LL))(*a3, a3);
        break;
      case 1952673648:
        v9 = qword_141B5FE40;
        sub_140FE7960(v13, a3, 1416914273);
        *(_QWORD *)(a1 + 64) = sub_140FA3700(v9, v13);
        break;
      case 1952671843:
        v6 = qword_141B5FDC0;
        sub_140FE7960(v13, a3, 1668246896);
        *(_QWORD *)(a1 + 24) = sub_140F7A940(v6, v13);
        break;
      default:
        return result;
    }
  }
  return 1;
}
