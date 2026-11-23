__int64 *__fastcall sub_141449D60(__int64 *a1, __int64 a2)
{
  int v4; // esi
  __int64 v5; // r14
  __int64 v6; // rdi
  int v7; // eax
  __int64 **v8; // rcx
  __int64 *v9; // r13
  __int64 *v10; // rcx
  __int64 v11; // r15
  _QWORD *v12; // rbx
  _QWORD *v13; // rbx
  __int64 v14; // rdi
  unsigned __int64 v15; // rax
  unsigned __int64 v16; // r14
  unsigned __int64 v17; // rcx
  unsigned __int64 v18; // r14
  __int64 v19; // rsi
  _QWORD *v20; // r15
  __int64 v21; // rdi
  unsigned __int64 v22; // rcx
  __int64 *v23; // r14
  __int64 v24; // r12
  unsigned __int64 v25; // rax
  unsigned __int64 v26; // rcx
  unsigned __int64 v27; // rax
  __int64 v28; // rdi
  _QWORD *v29; // rsi
  __int64 v30; // rsi
  unsigned __int64 v31; // rcx
  __int64 v32; // rbx
  __int64 v33; // rbx
  __int64 v34; // rbx
  __int64 v35; // rbx
  unsigned __int64 v37; // [rsp+20h] [rbp-30h]
  __int64 v38; // [rsp+28h] [rbp-28h]
  __int64 v39; // [rsp+30h] [rbp-20h]
  __int64 *v40; // [rsp+38h] [rbp-18h]
  unsigned __int64 v41; // [rsp+40h] [rbp-10h]
  unsigned __int64 v42; // [rsp+40h] [rbp-10h]
  int v43; // [rsp+48h] [rbp-8h]
  int v44; // [rsp+4Ch] [rbp-4h]

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
  v4 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a2 + 56LL))(a2);
  v5 = 0;
  v6 = 0;
  if ( v4 == 1 )
    v6 = a2;
  v7 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a2 + 56LL))(a2);
  if ( v7 == 3 )
    v5 = a2;
  v8 = *(__int64 ***)(qword_141B60208 + 128);
  v9 = *v8;
  v10 = v8[1];
  if ( v9 != v10 )
  {
    v43 = v4;
    v38 = v5;
    v39 = v6;
    v44 = v7;
    v40 = v10;
    do
    {
      v11 = *v9;
      if ( v4 != 1 || *(_QWORD *)(v11 + 24) != v6 )
        goto LABEL_16;
      v12 = (_QWORD *)a1[1];
      if ( v12 != (_QWORD *)a1[2] )
      {
        *v12 = v11;
        a1[1] += 8;
LABEL_16:
        if ( v7 != 3 )
          goto LABEL_11;
        goto LABEL_17;
      }
      v23 = a1;
      v24 = (__int64)v12 - *a1;
      v25 = (unsigned __int64)(v24 >> 3) >> 1;
      v26 = 0x1FFFFFFFFFFFFFFFLL - v25;
      v27 = (v24 >> 3) + v25;
      v42 = (v24 >> 3) + 1;
      if ( v27 <= v42 )
        v27 = (v24 >> 3) + 1;
      if ( v24 >> 3 > v26 )
        v27 = 0x1FFFFFFFFFFFFFFFLL;
      v37 = v27;
      v28 = sub_1407E4490(qword_141ABD470, 8 * v27);
      *(_QWORD *)(v28 + v24) = v11;
      v29 = (_QWORD *)v23[1];
      sub_141758A00();
      if ( v29 != v12 )
        sub_141758A00();
      v30 = *v23;
      a1 = v23;
      if ( *v23 != 0 )
      {
        v31 = v23[2] - v30;
        if ( v31 == -1 )
        {
          v31 = *(unsigned int *)(v30 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            goto LABEL_53;
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_53;
        }
        v34 = *(_QWORD *)(qword_141ABD470 + 24);
        if ( (*(_QWORD *)(qword_141ABD470 + 32) - v34) >> 3 <= v31 || (v35 = *(_QWORD *)(v34 + 8 * v31)) == 0 )
        {
LABEL_53:
          MEMORY[0x141948990](v30 - *(unsigned int *)(qword_141ABD470 + 48));
          goto LABEL_54;
        }
        MEMORY[0x1419475D8](v35 + 32, v30 - *(unsigned int *)(v35 + 120));
        if ( (*(_BYTE *)(v35 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v35 + 64)) == 0)
          && *(_BYTE *)(v35 + 97) != 0 )
        {
          sub_1412D33C0(v35);
        }
      }
LABEL_54:
      *v23 = v28;
      v23[1] = v28 + 8 * v42;
      v23[2] = v28 + 8 * v37;
      v4 = v43;
      v5 = v38;
      v6 = v39;
      v7 = v44;
      v10 = v40;
      if ( v44 != 3 )
        goto LABEL_11;
LABEL_17:
      if ( *(_QWORD *)(v11 + 32) == v5 )
      {
        v13 = (_QWORD *)a1[1];
        if ( v13 == (_QWORD *)a1[2] )
        {
          v14 = (__int64)v13 - *a1;
          v15 = v14 >> 3;
          v16 = (unsigned __int64)(v14 >> 3) >> 1;
          v17 = 0x1FFFFFFFFFFFFFFFLL - v16;
          v18 = (v14 >> 3) + v16;
          v41 = (v14 >> 3) + 1;
          if ( v18 <= v41 )
            v18 = v15 + 1;
          if ( v15 > v17 )
            v18 = 0x1FFFFFFFFFFFFFFFLL;
          v19 = sub_1407E4490(qword_141ABD470, 8 * v18);
          *(_QWORD *)(v19 + v14) = v11;
          v20 = (_QWORD *)a1[1];
          sub_141758A00();
          if ( v20 != v13 )
            sub_141758A00();
          v21 = *a1;
          if ( *a1 != 0 )
          {
            v22 = a1[2] - v21;
            if ( v22 == -1 )
            {
              v22 = *(unsigned int *)(v21 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                goto LABEL_45;
            }
            else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            {
              goto LABEL_45;
            }
            v32 = *(_QWORD *)(qword_141ABD470 + 24);
            if ( (*(_QWORD *)(qword_141ABD470 + 32) - v32) >> 3 > v22 && (v33 = *(_QWORD *)(v32 + 8 * v22)) != 0 )
            {
              MEMORY[0x1419475D8](v33 + 32, v21 - *(unsigned int *)(v33 + 120));
              if ( (*(_BYTE *)(v33 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v33 + 64)) == 0)
                && *(_BYTE *)(v33 + 97) != 0 )
              {
                sub_1412D33C0(v33);
              }
            }
            else
            {
LABEL_45:
              MEMORY[0x141948990](v21 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          *a1 = v19;
          a1[1] = v19 + 8 * v41;
          a1[2] = v19 + 8 * v18;
          v4 = v43;
          v5 = v38;
          v6 = v39;
          v7 = v44;
          v10 = v40;
          goto LABEL_11;
        }
        *v13 = v11;
        a1[1] += 8;
      }
LABEL_11:
      ++v9;
    }
    while ( v9 != v10 );
  }
  return a1;
}
