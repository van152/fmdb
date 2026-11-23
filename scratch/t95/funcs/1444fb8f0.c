__int64 *__fastcall sub_1444FB8F0(__int64 *a1, __int64 a2, char a3)
{
  __int64 v4; // rbx
  __int64 **v6; // rax
  __int64 *v7; // rsi
  __int64 *v8; // r14
  _QWORD *v9; // r13
  __int64 v10; // r15
  __int64 v11; // rcx
  __int64 *v12; // rdx
  char v13; // al
  __int64 v14; // rcx
  __int64 v15; // rcx
  __int64 v16; // r12
  unsigned __int64 v17; // rcx
  unsigned __int64 v18; // rax
  __int64 v19; // r8
  unsigned __int64 v20; // rdx
  unsigned __int64 v21; // rax
  __int64 v22; // rbx
  _QWORD *v23; // r15
  __int64 v24; // r12
  __int64 v25; // r8
  unsigned __int64 v26; // rcx
  __int64 v27; // rdi
  __int64 v28; // r15
  bool v29; // al
  unsigned __int64 v31; // [rsp+28h] [rbp-28h]
  __int64 v32; // [rsp+30h] [rbp-20h]
  __int64 *v34; // [rsp+40h] [rbp-10h]
  char v35; // [rsp+4Fh] [rbp-1h]

  v4 = a2;
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
        v4 = a2;
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  a1[2] = 0;
  a1[1] = 0;
  *a1 = 0;
  v6 = *(__int64 ***)(qword_141B601A0 + 128);
  v7 = *v6;
  v8 = v6[1];
  if ( *v6 != v8 )
  {
    v9 = nullptr;
    v35 = a3;
    v34 = a1;
    while ( 1 )
    {
      v10 = *v7;
      if ( *(_QWORD *)(*v7 + 32) == v4 )
      {
        v11 = *(_QWORD *)(v10 + 24);
        if ( v11 != 0 )
        {
          if ( a3 != -1 )
          {
            v12 = *(__int64 **)(v11 + 24);
            v13 = -1;
            if ( v12 != *(__int64 **)(v11 + 32) )
            {
              v14 = *v12;
              if ( *v12 != 0 && *(_QWORD *)(v14 + 48) != 0 )
              {
                v15 = *(_QWORD *)(v14 + 80);
                if ( v15 != 0 )
                  v13 = *(_BYTE *)(v15 + 418);
              }
            }
            if ( v13 != a3 )
              goto LABEL_8;
          }
          if ( v9 == (_QWORD *)a1[2] )
            break;
          *v9 = v10;
          v9 = (_QWORD *)(a1[1] + 8);
          a1[1] = (__int64)v9;
        }
      }
LABEL_8:
      if ( ++v7 == v8 )
        return a1;
    }
    v16 = (__int64)v9 - *a1;
    v17 = v16 >> 3;
    v18 = (unsigned __int64)(v16 >> 3) >> 1;
    v19 = 0x1FFFFFFFFFFFFFFFLL;
    v20 = 0x1FFFFFFFFFFFFFFFLL - v18;
    v21 = (v16 >> 3) + v18;
    v31 = (v16 >> 3) + 1;
    if ( v21 <= v31 )
      v21 = v17 + 1;
    if ( v17 <= v20 )
      v19 = v21;
    v32 = v19;
    v22 = sub_1407E4490(qword_141ABD470, 8 * v19);
    *(_QWORD *)(v22 + v16) = v10;
    a1 = v34;
    v23 = (_QWORD *)v34[1];
    sub_141758A00();
    if ( v23 != v9 )
      sub_141758A00();
    v24 = v22;
    v25 = *v34;
    v4 = a2;
    if ( *v34 == 0 )
    {
LABEL_35:
      *a1 = v24;
      v9 = (_QWORD *)(v24 + 8 * v31);
      a1[1] = (__int64)v9;
      a1[2] = v24 + 8 * v32;
      a3 = v35;
      goto LABEL_8;
    }
    v26 = v34[2] - v25;
    if ( v26 == -1 )
    {
      v26 = *(unsigned int *)(v25 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_34:
        MEMORY[0x141948990](v25 - *(unsigned int *)(qword_141ABD470 + 48));
        a1 = v34;
        goto LABEL_35;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_34;
    }
    v27 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v27) >> 3 > v26 )
    {
      v28 = *(_QWORD *)(v27 + 8 * v26);
      if ( v28 != 0 )
      {
        MEMORY[0x1419475D8](v28 + 32, v25 - *(unsigned int *)(v28 + 120));
        v29 = *(_BYTE *)(v28 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v28 + 64)) != 0;
        a1 = v34;
        if ( !v29 && *(_BYTE *)(v28 + 97) != 0 )
          sub_1412D33C0(v28);
        goto LABEL_35;
      }
    }
    goto LABEL_34;
  }
  return a1;
}
