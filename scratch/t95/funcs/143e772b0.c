__int64 __fastcall sub_143E772B0(_QWORD *a1, _DWORD **a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  _DWORD *v8; // rbx
  __int64 v9; // rax
  int v10; // eax
  _DWORD *v11; // rbx
  __int64 v12; // rax
  int v13; // eax
  _DWORD *v14; // rbx
  __int64 v15; // rax
  int v16; // eax
  _DWORD *v17; // rbx
  __int64 v18; // rax
  int v19; // eax
  _DWORD *v20; // rbx
  __int64 v21; // rax
  int v22; // eax
  _DWORD v24[9]; // [rsp+24h] [rbp-24h] BYREF

  v7 = *a2;
  LOBYTE(v24[0]) = 0;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v7 + 40LL))(v7, v24, 1);
  if ( v7[4] != 0 )
    return 0;
  v8 = *a2;
  v9 = a1[3];
  v10 = v9 != 0 ? *(_DWORD *)(v9 + 8) : -1;
  v24[0] = v10;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v8 + 40LL))(v8, v24, 4);
  if ( v8[4] != 0 )
    return 0;
  v11 = *a2;
  v12 = a1[4];
  v13 = v12 != 0 ? *(_DWORD *)(v12 + 8) : -1;
  v24[0] = v13;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v11 + 40LL))(v11, v24, 4);
  if ( v11[4] != 0 )
    return 0;
  v14 = *a2;
  v15 = a1[5];
  v16 = v15 != 0 ? *(_DWORD *)(v15 + 8) : -1;
  v24[0] = v16;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v14 + 40LL))(v14, v24, 4);
  if ( v14[4] != 0 )
    return 0;
  v17 = *a2;
  v18 = a1[6];
  v19 = v18 != 0 ? *(_DWORD *)(v18 + 8) : -1;
  v24[0] = v19;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v17 + 40LL))(v17, v24, 4);
  if ( v17[4] != 0 )
    return 0;
  v20 = *a2;
  v21 = a1[8];
  v22 = v21 != 0 ? *(_DWORD *)(v21 + 8) : -1;
  v24[0] = v22;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v20 + 40LL))(v20, v24, 4);
  if ( v20[4] != 0 )
    return 0;
  else
    return sub_140FE22B0(a1, a2, 0, a4);
}
