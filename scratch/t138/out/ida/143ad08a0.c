__int64 __fastcall sub_143AD08A0(__int64 a1, int a2)
{
  char v4; // bl
  void (__fastcall ***v5)(_QWORD, __int64); // rcx
  void (__fastcall ***v6)(_QWORD, __int64); // rcx
  __int64 v8; // [rsp+48h] [rbp-30h] BYREF
  __int64 v9; // [rsp+50h] [rbp-28h] BYREF
  _BYTE v10[32]; // [rsp+58h] [rbp-20h] BYREF

  sub_14080D0E0(a1: v10, a2: 0x1418E2C24LL);
  v8 = 0x80100004E554C4CLL;
  sub_1407D0F70(
    a1: (unsigned int)&v8,
    a2: (unsigned int)&v9,
    a3: a2,
    a4: (unsigned int)&qword_141B5BD88,
    a5: (__int64)v10,
    a6: 0,
    a7: 0,
    0);
  if ( v9 == 0 )
    goto LABEL_6;
  v8 = v9;
  _InterlockedIncrement((volatile signed __int32 *)(v9 + 8));
  v4 = sub_140CDFDA0(a1, a2: &v8);
  v5 = (void (__fastcall ***)(_QWORD, __int64))v8;
  if ( v8 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v8 + 8)) == 0 )
    (**v5)(a1: v5, a2: 1);
  if ( v4 == 0 )
    LODWORD(a1) = 0;
  else
LABEL_6:
    LOBYTE(a1) = 1;
  v6 = (void (__fastcall ***)(_QWORD, __int64))v9;
  if ( v9 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v9 + 8)) == 0 )
    (**v6)(a1: v6, a2: 1);
  return (unsigned int)a1;
}
