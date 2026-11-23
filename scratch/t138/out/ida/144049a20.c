__int64 *__fastcall sub_144049A20(__int64 a1, __int64 *a2, _WORD *a3)
{
  __int64 v5; // rax
  __int64 v6; // rcx
  void (__fastcall ***v7)(_QWORD, __int64); // rcx
  __int64 v9; // [rsp+48h] [rbp-30h] BYREF
  __int64 v10; // [rsp+50h] [rbp-28h] BYREF
  __int64 v11; // [rsp+58h] [rbp-20h] BYREF
  __int64 v12[3]; // [rsp+60h] [rbp-18h] BYREF

  v12[0] = 4096;
  v10 = 0x80100004E554C4CLL;
  sub_1407D0F70(a1: (unsigned int)&v10, (_DWORD)a2, a3: a1, a4: a1 + 16, a5: a1 + 32, a6: 0, a7: (__int64)v12, 1);
  *a3 = WORD2(v10);
  v5 = *a2;
  if ( *a2 != 0 && (_DWORD)v10 == 1667522932 )
  {
    v11 = *a2;
    _InterlockedIncrement((volatile signed __int32 *)(v5 + 8));
    sub_141219BF0(a1: &v9, a2: &v11);
    v6 = *a2;
    if ( *a2 == v9 )
    {
      if ( v6 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v6 + 8)) == 0 )
        (**(void (__fastcall ***)(__int64, __int64))v6)(a1: v6, a2: 1);
    }
    else
    {
      if ( v6 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v6 + 8)) == 0 )
        (**(void (__fastcall ***)(__int64, __int64))v6)(a1: v6, a2: 1);
      *a2 = v9;
      v9 = 0;
    }
    v7 = (void (__fastcall ***)(_QWORD, __int64))v11;
    if ( v11 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v11 + 8)) == 0 )
      (**v7)(a1: v7, a2: 1);
  }
  return a2;
}
