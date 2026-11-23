bool __fastcall sub_14474B9D0(_QWORD *a1, _QWORD *a2)
{
  __int64 v4; // rax
  __int64 v5; // rax
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  _BYTE v12[8]; // [rsp+20h] [rbp-38h] BYREF
  _BYTE v13[7]; // [rsp+28h] [rbp-30h] BYREF
  char v14; // [rsp+2Fh] [rbp-29h] BYREF
  int v15; // [rsp+30h] [rbp-28h] BYREF
  _DWORD v16[8]; // [rsp+38h] [rbp-20h] BYREF

  v4 = a1[2];
  if ( v4 != a1[3] )
    a1[3] = v4;
  v5 = a1[5];
  if ( v5 != a1[6] )
    a1[6] = v5;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v14, a3: 1);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return false;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 8, a3: 2);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return false;
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1, a3: 8);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return false;
  sub_141727D70(a1: v16, a2, a3: a1 + 2, a4: v12);
  if ( v16[0] != 0 )
    return false;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 66, a3: 2);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 1, a3: 8);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return false;
  sub_141727D70(a1: &v15, a2, a3: a1 + 5, a4: v13);
  return v15 == 0 && *(_DWORD *)(*a2 + 16LL) == 0;
}
