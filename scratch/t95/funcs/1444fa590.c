__int64 *__fastcall sub_1444FA590(__int64 *a1, __int64 a2)
{
  int v4; // eax
  int v5; // ecx
  __int64 **v6; // rax
  __int64 *v7; // rsi
  __int64 *v8; // r14
  __int64 v9; // r13
  __int64 v10; // rdi
  __int64 v11; // rbx
  _QWORD *v12; // rdi
  __int64 v13; // r15
  unsigned __int64 v14; // rax
  unsigned __int64 v15; // r14
  unsigned __int64 v16; // rcx
  unsigned __int64 v17; // r14
  __int64 v18; // rbx
  _QWORD *v19; // r13
  __int64 v20; // rdi
  unsigned __int64 v21; // rcx
  __int64 v22; // r8
  __int64 v23; // r15
  unsigned __int64 v25; // [rsp+28h] [rbp-18h]
  __int64 *v26; // [rsp+30h] [rbp-10h]
  int v27; // [rsp+38h] [rbp-8h] BYREF
  int v28; // [rsp+3Ch] [rbp-4h]
  __int64 v29; // [rsp+40h] [rbp+0h]

  v29 = -2;
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
  v4 = *(_DWORD *)(a2 + 12);
  v27 = v4;
  v5 = *(_DWORD *)(a2 + 16);
  if ( v5 == 0 )
    v5 = v4;
  v28 = v5;
  v6 = *(__int64 ***)(qword_141B60170 + 128);
  v7 = *v6;
  v8 = v6[1];
  if ( *v6 != v8 )
  {
    v26 = v6[1];
    while ( 1 )
    {
      v9 = *v7;
      if ( *v7 != 0 )
      {
        v10 = qword_141B5FDC0;
        if ( *(_DWORD *)(v9 + 32) != v27 || *(_DWORD *)(v9 + 36) != v28 )
        {
          v11 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)qword_141B5FDC0 + 32LL))(
                  qword_141B5FDC0,
                  v9 + 32);
          if ( v11 != (*(__int64 (__fastcall **)(__int64, int *))(*(_QWORD *)v10 + 32LL))(v10, &v27) )
            goto LABEL_9;
        }
        v12 = (_QWORD *)a1[1];
        if ( v12 == (_QWORD *)a1[2] )
          break;
        *v12 = v9;
        a1[1] += 8;
      }
LABEL_9:
      if ( ++v7 == v8 )
        return a1;
    }
    v13 = (__int64)v12 - *a1;
    v14 = v13 >> 3;
    v15 = (unsigned __int64)(v13 >> 3) >> 1;
    v16 = 0x1FFFFFFFFFFFFFFFLL - v15;
    v17 = (v13 >> 3) + v15;
    v25 = (v13 >> 3) + 1;
    if ( v17 <= v25 )
      v17 = v14 + 1;
    if ( v14 > v16 )
      v17 = 0x1FFFFFFFFFFFFFFFLL;
    v18 = sub_1407E4490(qword_141ABD470, 8 * v17);
    *(_QWORD *)(v18 + v13) = v9;
    v19 = (_QWORD *)a1[1];
    sub_141758A00();
    if ( v19 != v12 )
      sub_141758A00();
    v20 = *a1;
    if ( *a1 == 0 )
    {
LABEL_32:
      *a1 = v18;
      a1[1] = v18 + 8 * v25;
      a1[2] = v18 + 8 * v17;
      v8 = v26;
      goto LABEL_9;
    }
    v21 = a1[2] - v20;
    if ( v21 == -1 )
    {
      v21 = *(unsigned int *)(v20 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_31:
        MEMORY[0x141948990](v20 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_32;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_31;
    }
    v22 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v22) >> 3 > v21 )
    {
      v23 = *(_QWORD *)(v22 + 8 * v21);
      if ( v23 != 0 )
      {
        MEMORY[0x1419475D8](v23 + 32, v20 - *(unsigned int *)(v23 + 120));
        if ( (*(_BYTE *)(v23 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v23 + 64)) == 0)
          && *(_BYTE *)(v23 + 97) != 0 )
        {
          sub_1412D33C0(v23);
        }
        goto LABEL_32;
      }
    }
    goto LABEL_31;
  }
  return a1;
}
