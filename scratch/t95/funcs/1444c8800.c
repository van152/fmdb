__int64 *__fastcall sub_1444C8800(__int64 *a1, __int64 a2, char a3)
{
  __int64 **v6; // rax
  __int64 *v7; // rdi
  __int64 *v8; // r14
  _QWORD *v9; // rbx
  __int64 v10; // r15
  __int64 v11; // r12
  unsigned __int64 v12; // rcx
  unsigned __int64 v13; // rax
  __int64 v14; // r8
  unsigned __int64 v15; // rdx
  unsigned __int64 v16; // rax
  __int64 v17; // r13
  _QWORD *v18; // r15
  bool v19; // zf
  __int64 v20; // r15
  __int64 v21; // rbx
  __int64 v22; // r12
  unsigned __int64 v23; // rcx
  __int64 v24; // r8
  __int64 v25; // r15
  bool v26; // al
  unsigned __int64 v28; // [rsp+28h] [rbp-28h]
  __int64 *v29; // [rsp+30h] [rbp-20h]
  __int64 v30; // [rsp+38h] [rbp-18h]
  char v31; // [rsp+4Fh] [rbp-1h]

  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  a1[2] = 0;
  a1[1] = 0;
  *a1 = 0;
  v6 = *(__int64 ***)(qword_141B60190 + 128);
  v7 = *v6;
  v8 = v6[1];
  if ( *v6 != v8 )
  {
    v9 = nullptr;
    while ( 1 )
    {
      v10 = *v7;
      if ( *v7 != 0
        && *(_DWORD *)(v10 + 76) == *(_DWORD *)(a2 + 12)
        && *(_BYTE *)(v10 + 94) == 0xFF
        && (*(_BYTE *)(v10 + 91) == 79) != a3 )
      {
        if ( v9 == (_QWORD *)a1[2] )
          break;
        *v9 = v10;
        v9 = (_QWORD *)(a1[1] + 8);
        a1[1] = (__int64)v9;
      }
LABEL_7:
      if ( ++v7 == v8 )
        return a1;
    }
    v31 = a3;
    v29 = a1;
    v11 = (__int64)v9 - *a1;
    v12 = v11 >> 3;
    v13 = (unsigned __int64)(v11 >> 3) >> 1;
    v14 = 0x1FFFFFFFFFFFFFFFLL;
    v15 = 0x1FFFFFFFFFFFFFFFLL - v13;
    v16 = (v11 >> 3) + v13;
    v28 = (v11 >> 3) + 1;
    if ( v16 <= v28 )
      v16 = v12 + 1;
    if ( v12 <= v15 )
      v14 = v16;
    v30 = v14;
    v17 = sub_1407E4490(qword_141ABD470, 8 * v14);
    *(_QWORD *)(v17 + v11) = v10;
    v18 = (_QWORD *)v29[1];
    sub_141758A00();
    v19 = v18 == v9;
    v20 = v17;
    if ( !v19 )
      sub_141758A00();
    v21 = *v29;
    a1 = v29;
    v22 = v20;
    if ( *v29 == 0 )
    {
LABEL_29:
      *v29 = v22;
      v9 = (_QWORD *)(v22 + 8 * v28);
      v29[1] = (__int64)v9;
      v29[2] = v22 + 8 * v30;
      a3 = v31;
      goto LABEL_7;
    }
    v23 = v29[2] - v21;
    if ( v23 == -1 )
    {
      v23 = *(unsigned int *)(v21 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_28:
        MEMORY[0x141948990](v21 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_29;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_28;
    }
    v24 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v24) >> 3 > v23 )
    {
      v25 = *(_QWORD *)(v24 + 8 * v23);
      if ( v25 != 0 )
      {
        MEMORY[0x1419475D8](v25 + 32, v21 - *(unsigned int *)(v25 + 120));
        v26 = *(_BYTE *)(v25 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v25 + 64)) != 0;
        if ( !v26 && *(_BYTE *)(v25 + 97) != 0 )
          sub_1412D33C0(v25);
        goto LABEL_29;
      }
    }
    goto LABEL_28;
  }
  return a1;
}
