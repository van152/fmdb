__int64 __fastcall sub_1438ACE50(__int64 a1, __int64 a2)
{
  __int64 v4; // r9
  unsigned int v5; // ebx
  void (__fastcall ***v6)(_QWORD, __int64); // rcx
  __int64 v7; // rax
  __int64 v8; // rcx
  unsigned __int64 v9; // rsi
  void (__fastcall ***v10)(_QWORD, __int64); // rcx
  __int64 v11; // rcx
  __int64 v13; // [rsp+48h] [rbp-50h] BYREF
  __int64 v14; // [rsp+50h] [rbp-48h] BYREF
  __int64 v15; // [rsp+58h] [rbp-40h] BYREF
  __int64 v16; // [rsp+60h] [rbp-38h] BYREF
  _QWORD v17[6]; // [rsp+68h] [rbp-30h] BYREF

  v16 = 0;
  v17[0] = *(_QWORD *)(sub_140105F10() + 16);
  sub_1409698B0(a1, a2: &v16, a3: v17);
  v15 = 0x80100004E554C4CLL;
  sub_1407D0F70(
    a1: (unsigned int)&v15,
    a2: (unsigned int)&v14,
    a3: a2,
    a4: (unsigned int)&v16,
    a5: (__int64)v17,
    a6: 0,
    a7: 0,
    0);
  if ( v14 != 0 )
  {
    v4 = WORD2(v15);
    v13 = v14;
    _InterlockedIncrement((volatile signed __int32 *)(v14 + 8));
    v5 = sub_140969A30(a1, a2: &v13, a3: 0, a4: v4);
    v6 = (void (__fastcall ***)(_QWORD, __int64))v13;
    if ( v13 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13 + 8)) == 0 )
      (**v6)(a1: v6, a2: 1);
    v7 = *(_QWORD *)(a1 + 192);
    v8 = *(_QWORD *)(a1 + 200);
    if ( v8 != v7 )
    {
      v9 = 0;
      do
      {
        if ( (v5 & 1) != 0 )
        {
          v5 = sub_140969750(a1: *(_QWORD *)(v7 + 8 * v9), a2);
          v7 = *(_QWORD *)(a1 + 192);
          v8 = *(_QWORD *)(a1 + 200);
        }
        else
        {
          v5 = 0;
        }
        ++v9;
      }
      while ( v9 < (v8 - v7) >> 3 );
    }
    v10 = (void (__fastcall ***)(_QWORD, __int64))v14;
    if ( v14 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 8)) == 0 )
      (**v10)(a1: v10, a2: 1);
  }
  else
  {
    v5 = 0;
  }
  v11 = v16;
  if ( v16 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v16 - 4)) == 0 )
    sub_1412EC9A0(a1: v11 - 4);
  return v5;
}
