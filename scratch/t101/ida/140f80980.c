char __fastcall sub_140F80980(__int64 *a1, _QWORD *a2, char a3)
{
  __int64 v5; // rcx
  _DWORD *v6; // rbx
  int v7; // eax
  __int64 v8; // rbx
  char v10; // dl
  __int64 v11; // r8
  char v12; // r8
  __int64 *v13; // rcx
  _QWORD *v14; // rdx
  __int64 v15; // rbx
  unsigned __int64 v16; // rax
  _DWORD *v17; // rdi
  __int64 v18; // rcx
  __int64 *v19; // rbx
  __int64 v20; // rdx
  unsigned __int64 v21; // rbx
  __int64 *v22; // rcx
  __int64 v23; // rax
  char v24; // [rsp+26h] [rbp-22h] BYREF
  char v25; // [rsp+27h] [rbp-21h] BYREF
  unsigned int v26; // [rsp+28h] [rbp-20h] BYREF
  int v27[7]; // [rsp+2Ch] [rbp-1Ch] BYREF

  v5 = *a2;
  if ( (*(_BYTE *)(*a2 + 12LL) & 2) != 0 )
  {
    v10 = HIBYTE(qword_141B6034C);
    if ( BYTE6(qword_141B6034C) != 0 || a3 == 3 && (v10 = 1, HIBYTE(qword_141B6034C) != 0) )
    {
      if ( v10 == 0 || byte_141B5FC2C != 0 )
        v11 = 4;
      else
        v11 = 8;
      (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)v5 + 40LL))(v5, a1, v11);
      return 1;
    }
  }
  *a1 = 0;
  v6 = (_DWORD *)*a2;
  v7 = *(_DWORD *)(*a2 + 12LL);
  if ( (v7 & 2) != 0 )
  {
    v12 = (2 * ~(_BYTE)v7) & 4;
    if ( byte_141AAE088 == 0 )
      v12 = 0;
    v24 = v12;
    if ( v12 == 0 )
      goto LABEL_5;
LABEL_16:
    v13 = a1;
    v14 = a2;
    return sub_140F84C10(v13, v14);
  }
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)v6 + 40LL))(*a2, &v24, 1);
  if ( v6[4] != 0 )
    return 0;
  if ( v24 != 0 )
    goto LABEL_16;
LABEL_5:
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v25, 1);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return 0;
  if ( v25 == 2 )
  {
    v13 = a1;
    v14 = a2;
    return sub_140F84C10(v13, v14);
  }
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v27, 4);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return 0;
  v16 = (unsigned int)v27[0];
  if ( v27[0] == 0xFFFFFFFFLL )
  {
    *a1 = 0;
    return 1;
  }
  if ( v25 != 1 )
  {
    if ( v27[0] >= 0 )
    {
      v22 = *(__int64 **)(qword_141B5FE40 + 128);
      v20 = *v22;
      v21 = (v22[1] - *v22) >> 3;
LABEL_34:
      if ( v21 > v16 )
      {
        *a1 = *(_QWORD *)(v20 + 8 * v16);
        return 1;
      }
    }
    *a1 = 0;
    return 0;
  }
  v17 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, unsigned int *, __int64))(*(_QWORD *)v17 + 40LL))(v17, &v26, 4);
  if ( v17[4] != 0 )
    return 0;
  v16 = (unsigned int)v27[0];
  if ( v27[0] >= 0 )
  {
    v18 = qword_141B5FE40;
    v19 = *(__int64 **)(qword_141B5FE40 + 128);
    v20 = *v19;
    v21 = (v19[1] - *v19) >> 3;
    if ( v21 <= (unsigned int)v27[0] || *(_DWORD *)(*(_QWORD *)(v20 + 8LL * (unsigned int)v27[0]) + 12LL) != v26 )
      goto LABEL_38;
    goto LABEL_34;
  }
  v18 = qword_141B5FE40;
LABEL_38:
  v23 = sub_140F74650(v18, v26);
  *a1 = v23;
  return v23 != 0;
}
