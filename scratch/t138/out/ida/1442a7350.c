bool __fastcall sub_1442A7350(__int64 a1, _QWORD *a2)
{
  __int64 v4; // r15
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v8; // r14
  __int64 v9; // rbx
  __int64 v10; // r8
  __int64 v11; // rcx
  _DWORD *v12; // rdi
  __int64 v13[7]; // [rsp+20h] [rbp-38h] BYREF

  v4 = a1 + 8;
  if ( *(__int16 *)(a1 + 8) < 0 )
  {
    v8 = qword_141B5AD60;
    v13[0] = 0;
    v9 = sub_1412EC810(a1: 264, a2: 47);
    *(_QWORD *)v9 = 0x2F00000000LL;
    strcpy((char *)(v9 + 8), "invalid discipline rules index in booking count");
    if ( v13[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13[0] - 4)) == 0 )
      sub_1412EC9A0(a1: v13[0] - 4);
    v13[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v9);
    v13[0] = v9 + 4;
    LOBYTE(v10) = 1;
    (*(void (__fastcall **)(__int64, __int64 *, __int64, _QWORD))(*(_QWORD *)v8 + 120LL))(
      a1: v8,
      a2: v13,
      a3: v10,
      a4: 0);
    v11 = v13[0];
    if ( v13[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13[0] - 4)) == 0 )
      sub_1412EC9A0(a1: v11 - 4);
  }
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v4, a3: 2);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 10, a3: 1);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return false;
  v12 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v12 + 40LL))(a1: v12, a2: a1 + 11, a3: 1);
  return v12[4] == 0;
}
