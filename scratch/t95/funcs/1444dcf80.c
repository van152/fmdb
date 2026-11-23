__int64 __fastcall sub_1444DCF80(__int64 a1, int a2, _QWORD *a3)
{
  __int64 v6; // rbx
  __int64 v7; // rax
  __int64 v8; // rsi
  int v9; // ecx
  int v10; // eax
  __int64 v11; // rbx
  __int64 v12; // rdi
  int v13; // eax
  int v14; // ecx
  __int64 v15; // rsi
  char v16; // bp
  __int64 v17; // rbp
  __int64 v18; // rcx
  _DWORD *v19; // rsi
  __int64 v20; // rbp
  int v21; // eax
  int v22; // eax
  _QWORD v24[6]; // [rsp+28h] [rbp-30h] BYREF

  LODWORD(v6) = 0;
  v7 = sub_140FE84D0();
  if ( a2 > 1836345458 )
  {
    switch ( a2 )
    {
      case 1836345459:
        *(_DWORD *)(a1 + 48) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        break;
      case 1887005046:
        *(_BYTE *)(a1 + 56) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        break;
      case 1886151033:
        sub_140FE7960(v24, a3, 1348825715);
        *(_QWORD *)(a1 + 24) = v24[0];
        break;
      default:
        return (unsigned int)v6;
    }
LABEL_40:
    LOBYTE(v6) = 1;
    return (unsigned int)v6;
  }
  if ( a2 == 1667330920 )
  {
    *(_DWORD *)(a1 + 52) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
    goto LABEL_40;
  }
  v8 = v7;
  if ( a2 == 1668052322 )
  {
    v11 = qword_141B5FDB8;
    sub_140FE7960(v24, a3, 1130589301);
    v12 = sub_140F7A940(v11, v24);
    if ( v8 != 0 )
    {
      v13 = *(_DWORD *)(v8 + 12);
      LODWORD(v24[0]) = v13;
      v14 = *(_DWORD *)(v8 + 16);
      if ( v14 == 0 )
        v14 = v13;
    }
    else
    {
      LODWORD(v24[0]) = -1;
      v13 = -1;
      v14 = -1;
    }
    v6 = qword_141B5FDB8;
    HIDWORD(v24[0]) = v14;
    if ( v13 == *(_DWORD *)(a1 + 32) && v14 == *(_DWORD *)(a1 + 36)
      || (v19 = (_DWORD *)(a1 + 32),
          (v20 = (*(__int64 (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)qword_141B5FDB8 + 32LL))(
                   qword_141B5FDB8,
                   v24)) == (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v6 + 32LL))(v6, a1 + 32)) )
    {
      if ( v12 != 0 )
      {
        *(_DWORD *)(a1 + 40) = *(_DWORD *)(v12 + 12);
        v22 = *(_DWORD *)(v12 + 16);
        if ( v22 == 0 )
          v22 = *(_DWORD *)(v12 + 12);
      }
      else
      {
        *(_DWORD *)(a1 + 40) = -1;
        v22 = -1;
      }
      *(_DWORD *)(a1 + 44) = v22;
    }
    else
    {
      if ( v12 != 0 )
      {
        *v19 = *(_DWORD *)(v12 + 12);
        v21 = *(_DWORD *)(v12 + 16);
        if ( v21 == 0 )
          v21 = *(_DWORD *)(v12 + 12);
      }
      else
      {
        *v19 = -1;
        v21 = -1;
      }
      *(_DWORD *)(a1 + 36) = v21;
    }
    goto LABEL_40;
  }
  if ( a2 == 1768124269 )
  {
    if ( v7 != 0 )
    {
      v9 = *(_DWORD *)(v7 + 12);
      LODWORD(v24[0]) = v9;
      v10 = *(_DWORD *)(v7 + 16);
      if ( v10 == 0 )
        v10 = v9;
    }
    else
    {
      LODWORD(v24[0]) = -1;
      v9 = -1;
      v10 = -1;
    }
    v15 = qword_141B5FDB8;
    HIDWORD(v24[0]) = v10;
    if ( v9 != *(_DWORD *)(a1 + 40) || (v16 = 1, v10 != *(_DWORD *)(a1 + 44)) )
    {
      LODWORD(v6) = a1 + 40;
      v17 = (*(__int64 (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)qword_141B5FDB8 + 32LL))(qword_141B5FDB8, v24);
      v16 = v17 == (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v15 + 32LL))(v15, a1 + 40);
    }
    LOBYTE(v6) = 1;
    if ( v16 != (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3) )
    {
      v18 = *(_QWORD *)(a1 + 40);
      *(_QWORD *)(a1 + 40) = *(_QWORD *)(a1 + 32);
      *(_QWORD *)(a1 + 32) = v18;
    }
  }
  return (unsigned int)v6;
}
