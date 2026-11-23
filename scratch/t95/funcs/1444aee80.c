__int64 *__fastcall sub_1444AEE80(__int64 *a1, __int64 a2, char a3)
{
  __int64 **v6; // rax
  __int64 *v7; // rdi
  __int64 *v8; // r13
  _QWORD *v9; // r12
  __int64 v10; // r14
  unsigned __int8 v11; // al
  __int64 v12; // rax
  __int64 v13; // r15
  unsigned __int64 v14; // rcx
  unsigned __int64 v15; // rax
  __int64 v16; // r8
  unsigned __int64 v17; // rdx
  unsigned __int64 v18; // rax
  __int64 v19; // rbx
  _QWORD *v20; // r14
  __int64 v21; // r15
  __int64 v22; // rbx
  unsigned __int64 v23; // rcx
  __int64 v24; // r8
  __int64 v25; // r14
  unsigned __int64 v27; // [rsp+28h] [rbp-18h]
  __int64 v28; // [rsp+30h] [rbp-10h]
  __int64 v29; // [rsp+38h] [rbp-8h]

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
  *((_BYTE *)a1 + 24) = a3;
  v6 = *(__int64 ***)(qword_141B60118 + 128);
  v7 = *v6;
  v8 = v6[1];
  if ( *v6 != v8 )
  {
    v9 = nullptr;
    v29 = a2;
    do
    {
      v10 = *v7;
      v11 = *(_BYTE *)(*v7 + 94);
      if ( *((_BYTE *)a1 + 24) != 0 )
      {
        if ( v11 != 0xFD )
          goto LABEL_7;
      }
      else if ( v11 == 0xFD || v11 == 0 || v11 == 251 )
      {
        goto LABEL_7;
      }
      v12 = *(_QWORD *)(v10 + 24);
      if ( v12 == 0 || *(_DWORD *)(v12 + 12) != *(_DWORD *)(a2 + 12) )
        goto LABEL_7;
      if ( v9 == (_QWORD *)a1[2] )
      {
        v13 = (__int64)v9 - *a1;
        v14 = v13 >> 3;
        v15 = (unsigned __int64)(v13 >> 3) >> 1;
        v16 = 0x1FFFFFFFFFFFFFFFLL;
        v17 = 0x1FFFFFFFFFFFFFFFLL - v15;
        v18 = (v13 >> 3) + v15;
        v27 = (v13 >> 3) + 1;
        if ( v18 <= v27 )
          v18 = v14 + 1;
        if ( v14 <= v17 )
          v16 = v18;
        v28 = v16;
        v19 = sub_1407E4490(qword_141ABD470, 8 * v16);
        *(_QWORD *)(v19 + v13) = v10;
        v20 = (_QWORD *)a1[1];
        sub_141758A00();
        if ( v20 != v9 )
          sub_141758A00();
        v21 = v19;
        v22 = *a1;
        if ( *a1 != 0 )
        {
          v23 = a1[2] - v22;
          if ( v23 == -1 )
          {
            v23 = *(unsigned int *)(v22 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
              goto LABEL_33;
          }
          else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
          {
            goto LABEL_33;
          }
          v24 = *(_QWORD *)(qword_141ABD470 + 24);
          if ( (*(_QWORD *)(qword_141ABD470 + 32) - v24) >> 3 > v23 && (v25 = *(_QWORD *)(v24 + 8 * v23)) != 0 )
          {
            MEMORY[0x1419475D8](v25 + 32, v22 - *(unsigned int *)(v25 + 120));
            if ( (*(_BYTE *)(v25 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v25 + 64)) == 0)
              && *(_BYTE *)(v25 + 97) != 0 )
            {
              sub_1412D33C0(v25);
            }
          }
          else
          {
LABEL_33:
            MEMORY[0x141948990](v22 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        *a1 = v21;
        v9 = (_QWORD *)(v21 + 8 * v27);
        a1[1] = (__int64)v9;
        a1[2] = v21 + 8 * v28;
        a2 = v29;
        goto LABEL_7;
      }
      *v9 = v10;
      v9 = (_QWORD *)(a1[1] + 8);
      a1[1] = (__int64)v9;
LABEL_7:
      ++v7;
    }
    while ( v7 != v8 );
  }
  return a1;
}
