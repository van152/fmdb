__int64 __fastcall sub_14438A850(__int64 **a1, __int64 a2)
{
  __int64 v3; // rax
  __int64 v4; // rdi
  __int64 v5; // rbx
  unsigned __int64 v6; // r13
  __int64 v7; // rcx
  __int64 v8; // rax
  __int64 v9; // rdx
  __int64 *v10; // rsi
  __int64 *v11; // rdx
  int v12; // eax
  __int64 v13; // rsi
  __int64 v14; // rdi
  __int64 v15; // rax
  __int64 v16; // r8
  char v17; // cl
  __int64 v18; // r14
  __int64 v19; // rdi
  __int64 v20; // rax
  __int64 v21; // r8
  char v22; // bl
  __int64 v25; // [rsp+30h] [rbp-10h] BYREF
  __int64 v26; // [rsp+38h] [rbp-8h]
  __int64 v27; // [rsp+40h] [rbp+0h]

  v27 = -2;
  v3 = **a1;
  v4 = *(_QWORD *)(v3 + 48);
  v5 = *(_QWORD *)(v3 + 56);
  v6 = (v5 - v4) >> 4;
  v7 = qword_141B60C38;
  v8 = qword_141B60C30;
  if ( qword_141B60C30 == qword_141B60C38 )
    goto LABEL_22;
  v9 = qword_141B60C30;
  while ( *(_DWORD *)v9 != 1684171881 )
  {
    v9 += 16;
    if ( v9 == qword_141B60C38 )
      goto LABEL_22;
  }
  if ( v9 == qword_141B60C38 || *(_QWORD *)(v9 + 8) == 0 )
    goto LABEL_22;
  v10 = nullptr;
  while ( *(_DWORD *)v8 != 1684171881 )
  {
    v8 += 16;
    if ( v8 == qword_141B60C38 )
      goto LABEL_15;
  }
  v10 = v8 == qword_141B60C38 ? nullptr : *(__int64 **)(v8 + 8);
LABEL_15:
  v11 = &qword_141B5A4A0;
  if ( v10 != nullptr )
    v11 = v10;
  v12 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v11 + 64LL))(*v11);
  LODWORD(v13) = v12;
  if ( v12 < 0 || v6 <= (unsigned int)v12 )
  {
LABEL_22:
    if ( v5 == v4 )
    {
LABEL_29:
      LODWORD(v13) = -1;
      return (unsigned int)v13;
    }
LABEL_23:
    v18 = 0;
    v13 = 0;
    while ( 1 )
    {
      v19 = *(_QWORD *)(**a1 + 48);
      v20 = sub_14083D4F0(v7) + 8;
      v26 = 0;
      v25 = v20;
      if ( v19 != 0 )
      {
        LOBYTE(v21) = 1;
        sub_14145B4C0(v18 + v19, &v25, v21);
        v22 = sub_140DD6070(a2, &v25, 0);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v25 + 16LL))(v25, &v25);
        if ( v22 != 0 )
          return (unsigned int)v13;
      }
      else
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v20 + 16LL))(v20, &v25);
      }
      ++v13;
      v18 += 16;
      if ( v6 == v13 )
        goto LABEL_29;
    }
  }
  v14 = *(_QWORD *)(**a1 + 48);
  v15 = sub_14083D4F0(v7) + 8;
  v26 = 0;
  v25 = v15;
  if ( v14 == 0
    || (LOBYTE(v16) = 1,
        sub_14145B4C0(16LL * (unsigned int)v13 + v14, &v25, v16),
        v17 = sub_140DD6070(a2, &v25, 0),
        v15 = v25,
        v17 == 0) )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v15 + 16LL))(v15, &v25);
    goto LABEL_23;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v25 + 16LL))(v25, &v25);
  return (unsigned int)v13;
}
