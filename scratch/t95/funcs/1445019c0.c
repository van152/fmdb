__int64 __fastcall sub_1445019C0(_QWORD *a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  _DWORD *v8; // rbx
  __int64 v9; // rax
  int v10; // eax
  _DWORD *v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // r14
  __int64 v14; // rbx
  unsigned __int64 v15; // r14
  __int64 v16; // rbx
  char v18; // [rsp+23h] [rbp-35h] BYREF
  int v19; // [rsp+24h] [rbp-34h] BYREF
  int v20; // [rsp+28h] [rbp-30h] BYREF
  _DWORD v21[11]; // [rsp+2Ch] [rbp-2Ch] BYREF

  v7 = (_DWORD *)*a2;
  v18 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v7 + 40LL))(v7, &v18, 1);
  if ( v7[4] != 0 )
    return 0;
  v8 = (_DWORD *)*a2;
  v9 = a1[3];
  v10 = v9 != 0 ? *(_DWORD *)(v9 + 8) : -1;
  v19 = v10;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v8 + 40LL))(v8, &v19, 4);
  if ( v8[4] != 0 )
    return 0;
  v11 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 4, 4);
  if ( v11[4] != 0 )
    return 0;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 36, 4);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return 0;
  v13 = a1[9] - a1[8];
  v20 = *((_DWORD *)a1 + 18) - *((_DWORD *)a1 + 16);
  (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v20, 4);
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1[8], v13);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return 0;
  v15 = a1[6] - a1[5];
  v21[0] = v15 >> 1;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v21, 4);
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD, unsigned __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1[5], v15);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return 0;
  else
    return sub_140FE22B0(a1, a2, 0, a4);
}
