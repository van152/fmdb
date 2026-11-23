__int64 __fastcall sub_143A26F90(_QWORD *a1, __int64 a2)
{
  __int64 v4; // rax
  __int64 v5; // rcx
  __int64 v6; // rbx
  __int64 v7; // rax
  __int64 v8; // rsi
  __int64 v9; // rax
  __int64 v10; // rcx
  unsigned int v11; // ebx
  __int64 v12; // rbx
  __int64 v13; // rcx
  void (__fastcall ***v14)(_QWORD, __int64); // rcx
  void (__fastcall ***v15)(_QWORD, __int64); // rcx
  __int64 v16; // rax
  unsigned __int64 v17; // rsi
  void (__fastcall ***v18)(_QWORD, __int64); // rcx
  __int64 v20; // [rsp+48h] [rbp-40h] BYREF
  __int64 v21; // [rsp+50h] [rbp-38h] BYREF
  __int64 v22; // [rsp+58h] [rbp-30h] BYREF
  __int64 v23; // [rsp+60h] [rbp-28h] BYREF

  v4 = sub_140F45DB0(a1: qword_141B5FDC0);
  if ( v4 != 0 )
    v5 = *(_QWORD *)(v4 + 176);
  else
    v5 = 0;
  v6 = 0;
  a1[2] = sub_141758910(a1: v5, a2: 0, a3: &unk_141A80850, a4: &unk_141AAB3C0, a5: 0);
  v7 = sub_140F45DB0(a1: qword_141B5FDC0);
  if ( v7 != 0 )
    v6 = *(_QWORD *)(v7 + 176);
  v8 = 0;
  a1[3] = sub_141758910(a1: v6, a2: 0, a3: &unk_141A80850, a4: &unk_141AAB3C0, a5: 0);
  if ( sub_140F45DB0(a1: qword_141B5FDC0) != 0 )
  {
    v9 = sub_140F45DB0(a1: qword_141B5FDC0);
    if ( v9 != 0 )
      v10 = *(_QWORD *)(v9 + 176);
    else
      v10 = 0;
    v8 = sub_141758910(a1: v10, a2: 0, a3: &unk_141A80850, a4: &unk_141AAB3C0, a5: 0);
  }
  a1[4] = v8;
  v11 = 0;
  if ( a1[2] != 0 && a1[3] != 0 )
  {
    v23 = 0x80100004E554C4CLL;
    sub_14080D0E0(a1: &v22, a2: 0x1418E2C24LL);
    v12 = sub_1412EC810(a1: 264, a2: 10);
    *(_QWORD *)v12 = 0xA00000000LL;
    strcpy((char *)(v12 + 8), "friend_man");
    _InterlockedIncrement((volatile signed __int32 *)v12);
    v21 = 0;
    _InterlockedIncrement((volatile signed __int32 *)v12);
    v21 = v12 + 4;
    sub_1407D0F70(
      a1: (unsigned int)&v23,
      a2: (unsigned int)&v20,
      a3: a2,
      a4: (unsigned int)&v21,
      a5: (__int64)&v22,
      a6: 0,
      a7: 0,
      0);
    v13 = v21;
    if ( v21 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v21 - 4)) == 0 )
      sub_1412EC9A0(a1: v13 - 4);
    if ( _InterlockedDecrement((volatile signed __int32 *)v12) == 0 )
      sub_1412EC9A0(a1: v12);
    if ( v20 == 0 )
      return 0;
    word_141AAB3B0 = WORD2(v23);
    v22 = v20;
    _InterlockedIncrement((volatile signed __int32 *)(v20 + 8));
    v11 = (*(__int64 (__fastcall **)(_QWORD *, __int64 *))(*a1 + 152LL))(a1, a2: &v22);
    v14 = (void (__fastcall ***)(_QWORD, __int64))v22;
    if ( v22 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v22 + 8)) == 0 )
      (**v14)(a1: v14, a2: 1);
    if ( (_BYTE)v11 != 0 )
    {
      v15 = (void (__fastcall ***)(_QWORD, __int64))v20;
      if ( v20 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v20 + 8)) == 0 )
        (**v15)(a1: v15, a2: 1);
      v20 = 0;
      v16 = a1[5];
      if ( a1[6] == v16 )
      {
LABEL_30:
        word_141AAB3B0 = 32;
        LOBYTE(v11) = 1;
LABEL_32:
        v18 = (void (__fastcall ***)(_QWORD, __int64))v20;
        if ( v20 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v20 + 8)) == 0 )
          (**v18)(a1: v18, a2: 1);
        return v11;
      }
      v17 = 0;
      while ( (unsigned __int8)sub_140969750(a1: *(_QWORD *)(v16 + 8 * v17), a2) != 0 )
      {
        ++v17;
        v16 = a1[5];
        if ( v17 >= (a1[6] - v16) >> 3 )
          goto LABEL_30;
      }
    }
    v11 = 0;
    goto LABEL_32;
  }
  return v11;
}
