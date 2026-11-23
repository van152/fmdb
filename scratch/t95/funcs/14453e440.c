bool __fastcall sub_14453E440(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  _DWORD *v5; // rbx
  __int64 v6; // rax
  int v7; // eax
  _DWORD *v8; // rbx
  _DWORD *v9; // rbx
  __int64 v10; // rax
  unsigned __int64 v11; // rsi
  __int64 v12; // r15
  __int64 v13; // rbx
  __int64 v14; // rbx
  __int64 v15; // rbx
  __int64 v16; // rbx
  __int64 v17; // rbx
  _DWORD *v18; // rdi
  __int64 v19; // rdx
  char v21; // [rsp+2Fh] [rbp-39h] BYREF
  int v22; // [rsp+30h] [rbp-38h] BYREF
  _DWORD v23[13]; // [rsp+34h] [rbp-34h] BYREF

  v4 = (_DWORD *)*a2;
  v21 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v4 + 40LL))(v4, &v21, 1);
  if ( v4[4] != 0 )
    return false;
  v5 = (_DWORD *)*a2;
  v6 = *(_QWORD *)(a1 + 48);
  v7 = v6 != 0 ? *(_DWORD *)(v6 + 8) : -1;
  v23[0] = v7;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v5 + 40LL))(v5, v23, 4);
  if ( v5[4] != 0 )
    return false;
  v8 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 56, 1);
  if ( v8[4] != 0 )
    return false;
  v9 = (_DWORD *)*a2;
  v22 = (*(_QWORD *)(a1 + 32) - *(_QWORD *)(a1 + 24)) >> 3;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v9 + 40LL))(v9, &v22, 4);
  if ( v9[4] != 0 )
    return false;
  v10 = *(_QWORD *)(a1 + 24);
  if ( *(_QWORD *)(a1 + 32) != v10 )
  {
    v11 = 0;
    do
    {
      v12 = *(_QWORD *)(v10 + 8 * v11);
      v13 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, 0x1418BDE61LL, 1);
      if ( *(_DWORD *)(v13 + 16) == 0 )
      {
        v14 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v12, 4);
        if ( *(_DWORD *)(v14 + 16) == 0 )
        {
          v15 = *a2;
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v12 + 4, 4);
          if ( *(_DWORD *)(v15 + 16) == 0 )
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v12 + 8, 1);
        }
      }
      ++v11;
      v10 = *(_QWORD *)(a1 + 24);
    }
    while ( v11 < (*(_QWORD *)(a1 + 32) - v10) >> 3 );
  }
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return false;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return false;
  v18 = (_DWORD *)*a2;
  v19 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v18 + 40LL))(v18, v19, 4);
  return v18[4] == 0;
}
