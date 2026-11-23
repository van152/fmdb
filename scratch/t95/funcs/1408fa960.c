// THUNK ALIAS -> sub_143860CC0 (jmp:0x1408fa960->0x143860cc0)
__int64 __fastcall sub_143860CC0(__int64 a1, unsigned __int8 a2, unsigned __int8 a3, char a4)
{
  __int64 v6; // rsi
  __int64 *v7; // rax
  __int64 v8; // rbx
  __int64 v9; // rbp
  __int64 v10; // r8
  __int64 v11; // rcx
  __int64 v12; // rax
  __int64 v13; // rcx
  __int64 v14; // rsi
  __int64 result; // rax
  char v16; // cl
  __int64 v17[7]; // [rsp+20h] [rbp-38h] BYREF

  v6 = a1;
  if ( a4 != 0 )
  {
    v7 = *(__int64 **)(a1 + 192);
    if ( v7 == *(__int64 **)(a1 + 200) )
      return 0;
    v6 = *v7;
  }
  if ( (unsigned __int8)(a2 + 1) >= 0x33u )
  {
    v8 = qword_141B5AD60;
    v17[0] = 0;
    v9 = sub_1412EC810(264, 24);
    *(_QWORD *)v9 = 0x1800000000LL;
    strcpy((char *)(v9 + 8), "suspect main stage index");
    if ( v17[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v17[0] - 4)) == 0 )
      sub_1412EC9A0(v17[0] - 4);
    v17[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v9);
    v17[0] = v9 + 4;
    LOBYTE(v10) = 1;
    (*(void (__fastcall **)(__int64, __int64 *, __int64, _QWORD))(*(_QWORD *)v8 + 120LL))(v8, v17, v10, 0);
    v11 = v17[0];
    if ( v17[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v17[0] - 4)) == 0 )
      sub_1412EC9A0(v11 - 4);
  }
  if ( (a2 & 0x80u) != 0 )
    return 0;
  v12 = *(_QWORD *)(v6 + 448);
  if ( (*(_QWORD *)(v6 + 456) - v12) >> 3 <= (unsigned __int64)a2 )
    return 0;
  v13 = *(_QWORD *)(v12 + 8LL * a2);
  if ( v13 == 0 )
    return 0;
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v13 + 656LL))(v13) == 6 )
    return 0;
  v14 = *(_QWORD *)(*(_QWORD *)(v6 + 448) + 8LL * a2);
  if ( v14 == 0 || (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v14 + 616LL))(v14) != 0 )
    return 0;
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v14 + 632LL))(v14) != 0 )
  {
    if ( (a3 & 0x80u) == 0 && (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v14 + 784LL))(v14) > (unsigned __int64)a3 )
      return (*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v14 + 808LL))(v14, a3);
    return 0;
  }
  v16 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v14 + 624LL))(v14);
  result = 0;
  if ( v16 != 0 )
    return v14;
  return result;
}
