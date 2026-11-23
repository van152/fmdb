__int64 __fastcall sub_1445442A0(__int64 a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  _DWORD *v8; // rbx
  __int64 v9; // rax
  int v10; // eax
  _DWORD *v11; // rbx
  __int64 v12; // rax
  int v13; // eax
  _DWORD *v14; // rbx
  __int64 v15; // rbx
  __int64 v16; // rbx
  char v18; // [rsp+2Fh] [rbp-29h] BYREF
  int v19; // [rsp+30h] [rbp-28h] BYREF
  _DWORD v20[9]; // [rsp+34h] [rbp-24h] BYREF

  v7 = (_DWORD *)*a2;
  v18 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v7 + 40LL))(v7, &v18, 1);
  if ( v7[4] != 0 )
    return 0;
  v8 = (_DWORD *)*a2;
  v9 = *(_QWORD *)(a1 + 24);
  v10 = v9 != 0 ? *(_DWORD *)(v9 + 8) : -1;
  v20[0] = v10;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v8 + 40LL))(v8, v20, 4);
  if ( v8[4] != 0 )
    return 0;
  v11 = (_DWORD *)*a2;
  v12 = *(_QWORD *)(a1 + 32);
  v13 = v12 != 0 ? *(_DWORD *)(v12 + 8) : -1;
  v19 = v13;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v11 + 40LL))(v11, &v19, 4);
  if ( v11[4] != 0 )
    return 0;
  v14 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 44, 2);
  if ( v14[4] != 0 )
    return 0;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 46, 1);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return 0;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 40, 4);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return 0;
  else
    return sub_140FE22B0(a1, a2, 0, a4);
}
