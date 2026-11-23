__int64 __fastcall sub_143AD0D70(__int64 a1, _QWORD *a2)
{
  int v4; // r9d
  void (__fastcall ***v5)(_QWORD, __int64); // rcx
  unsigned int v6; // esi
  void (__fastcall ***v7)(_QWORD, __int64); // rcx
  __int64 v9; // [rsp+28h] [rbp-28h] BYREF
  _BYTE v10[8]; // [rsp+30h] [rbp-20h] BYREF
  __int64 v11; // [rsp+38h] [rbp-18h] BYREF
  _QWORD v12[4]; // [rsp+40h] [rbp-10h] BYREF

  v12[1] = -2;
  sub_14080D0E0(a1: v10, a2: 0x1418E2C24LL);
  v9 = 0x80100004E554C4CLL;
  if ( *a2 == 0 )
    return 0;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64 *, _BYTE *))(*(_QWORD *)*a2 + 224LL))(
    a1: *a2,
    a2: v12,
    a3: &qword_141B5BD88,
    a4: v10);
  if ( v12[0] == 0 )
    return 0;
  LOWORD(v4) = 3;
  sub_1407D1280(a1: (unsigned int)&v9, a2: (unsigned int)&v11, a3: (unsigned int)v12, a4: v4, a5: 0);
  v5 = (void (__fastcall ***)(_QWORD, __int64))v12[0];
  if ( v12[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v12[0] + 8LL)) == 0 )
    (**v5)(a1: v5, a2: 1);
  if ( v11 != 0 )
  {
    v6 = sub_140CE0590(a1, a2: &v11);
    v7 = (void (__fastcall ***)(_QWORD, __int64))v11;
    if ( v11 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v11 + 8)) == 0 )
      (**v7)(a1: v7, a2: 1);
  }
  else
  {
    return 0;
  }
  return v6;
}
