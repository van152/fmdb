__int64 __fastcall sub_1438361D0(_BYTE *a1, _QWORD *a2)
{
  volatile signed __int32 *v4; // rdi
  __int64 v5; // rdx
  __int64 v6; // r8
  unsigned int v7; // edi
  volatile signed __int32 *v8; // rcx
  __int64 v9; // rsi
  __int64 v10; // rcx
  __int64 v11; // rcx
  void (__fastcall ***v12)(_QWORD, __int64); // rcx
  volatile signed __int32 *v14; // rdi
  char v15; // bl
  void (__fastcall ***v16)(_QWORD, __int64); // rcx
  volatile signed __int32 *v17; // rcx
  __int64 v18; // [rsp+40h] [rbp-38h] BYREF
  volatile signed __int32 *v19; // [rsp+48h] [rbp-30h] BYREF
  __int64 v20; // [rsp+50h] [rbp-28h] BYREF
  _QWORD v21[4]; // [rsp+58h] [rbp-20h] BYREF

  (*(void (__fastcall **)(_BYTE *))(*(_QWORD *)a1 + 760LL))(a1);
  (*(void (__fastcall **)(_QWORD, __int64 *, __int64 *, __int64 *))(*(_QWORD *)*a2 + 208LL))(
    a1: *a2,
    a2: &v20,
    a3: &qword_141B5ACF0,
    a4: &qword_141B59858);
  if ( v20 == 0 )
  {
    v18 = 0;
    v9 = sub_1412EC810(a1: 264, a2: 67);
    *(_QWORD *)v9 = 0x4300000000LL;
    sub_1417589F0(a1: v9 + 8, a2: 0x1418F3680LL, a3: 67);
    *(_BYTE *)(v9 + 75) = 0;
    v10 = v18;
    if ( v18 != 0 )
    {
      v10 = v18 - 4;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v18 - 4)) == 0 )
        sub_1412EC9A0(a1: v10);
    }
    v18 = 0;
    _InterlockedIncrement((volatile signed __int32 *)v9);
    v18 = v9 + 4;
    LOBYTE(v10) = 1;
    sub_1407E0E00(a1: v10, a2: &v18, a3: 0);
    v11 = v18;
    if ( v18 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v18 - 4)) == 0 )
      sub_1412EC9A0(a1: v11 - 4);
    goto LABEL_14;
  }
  sub_14080D0E0(a1: v21, a2: 0x1418E2C24LL);
  sub_1407D0F70(
    a1: (unsigned int)&v18,
    a2: (unsigned int)&v19,
    a3: (unsigned int)&v20,
    a4: (unsigned int)&qword_141B5ACB0,
    a5: (__int64)v21,
    a6: 0,
    a7: 0,
    0,
    0x80100004E554C4CLL);
  v4 = v19;
  if ( v19 == nullptr )
  {
LABEL_14:
    v7 = 0;
    goto LABEL_15;
  }
  word_141AAA410 = WORD2(v18);
  (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)v19 + 40LL))(
    a1: v19,
    a2: &word_141AAA412,
    a3: 2);
  if ( *((_DWORD *)v4 + 4) != 0
    || (unsigned __int16)word_141AAA410 >= 0x5E2u
    && (v14 = v19,
        (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v19 + 40LL))(
          a1: v19,
          a2: v21,
          a3: 2),
        *((_DWORD *)v14 + 4) != 0)
    || (unsigned __int16)word_141AAA412 < 0x5C8u
    || (unsigned __int16)word_141AAA410 < 0x5CDu )
  {
LABEL_4:
    v7 = 0;
    goto LABEL_5;
  }
  v7 = 0;
  if ( (unsigned __int16)word_141AAA412 <= 0x600u && (unsigned __int16)word_141AAA410 <= 0x600u )
  {
    LOBYTE(v5) = 1;
    LOBYTE(v6) = 1;
    (*(void (__fastcall **)(_BYTE *, __int64, __int64, _QWORD))(*(_QWORD *)a1 + 600LL))(a1, a2: v5, a3: v6, a4: 0);
    v21[0] = v19;
    if ( v19 != nullptr )
      _InterlockedIncrement(v19 + 2);
    v15 = (*(__int64 (__fastcall **)(_BYTE *, _QWORD *))(*(_QWORD *)a1 + 1856LL))(a1, a2: v21);
    v16 = (void (__fastcall ***)(_QWORD, __int64))v21[0];
    if ( v21[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v21[0] + 8LL)) == 0 )
      (**v16)(a1: v16, a2: 1);
    if ( v15 != 0 )
    {
      v17 = v19;
      if ( v19 != nullptr && _InterlockedDecrement(v19 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v17)(a1: v17, a2: 1);
      v19 = nullptr;
      if ( (*(unsigned __int8 (__fastcall **)(_BYTE *, __int64 *))(*(_QWORD *)a1 + 1872LL))(a1, a2: &v20) != 0
        && (unsigned __int8)sub_1408A4570(a1, a2: (__int64)&v20) != 0 )
      {
        a1[64] = 1;
        word_141AAA410 = 1536;
        sub_1409DC040();
        sub_14088FEF0();
        LOBYTE(v7) = 1;
        goto LABEL_5;
      }
    }
    goto LABEL_4;
  }
LABEL_5:
  v8 = v19;
  if ( v19 != nullptr && _InterlockedDecrement(v19 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v8)(a1: v8, a2: 1);
LABEL_15:
  v12 = (void (__fastcall ***)(_QWORD, __int64))v20;
  if ( v20 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v20 + 8)) == 0 )
    (**v12)(a1: v12, a2: 1);
  return v7;
}
