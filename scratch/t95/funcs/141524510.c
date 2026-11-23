__int64 *__fastcall sub_141524510(__int64 *a1, _DWORD *a2)
{
  int v4; // ecx
  int v5; // edx
  __int64 v6; // rax
  _QWORD *v7; // rbx
  _QWORD *v8; // r14
  _QWORD *v9; // rdi
  _DWORD *v10; // r13
  __int64 v11; // rsi
  __int64 v12; // rdi
  __int64 v13; // rsi
  __int64 v14; // rdi
  __int64 *v15; // r12
  __int64 v16; // r15
  unsigned __int64 v17; // r14
  unsigned __int64 v18; // rcx
  unsigned __int64 v19; // r14
  __int64 v20; // rsi
  _QWORD *v21; // r13
  __int64 v22; // r13
  __int64 v23; // rsi
  unsigned __int64 v24; // rcx
  __int64 v25; // rdi
  __int64 v26; // rdi
  __int64 v28[2]; // [rsp+28h] [rbp-38h] BYREF
  unsigned __int64 v29; // [rsp+38h] [rbp-28h]
  _QWORD *v30; // [rsp+40h] [rbp-20h]
  int v31; // [rsp+48h] [rbp-18h] BYREF
  int v32; // [rsp+4Ch] [rbp-14h]
  _QWORD v33[10]; // [rsp+50h] [rbp-10h] BYREF

  v33[2] = -2;
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
  (*(void (__fastcall **)(_DWORD *, int *))(*(_QWORD *)a2 + 144LL))(a2, &v31);
  sub_140FEAD00(&v31, v28);
  sub_140835380(&qword_141B60C30, 1130589301, v28);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v28[0] + 16LL))(v28[0], v28);
  (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v33[0] + 16LL))(v33[0], v33);
  v4 = a2[3];
  v31 = v4;
  v5 = a2[4];
  if ( v5 == 0 )
    v5 = v4;
  v32 = v5;
  v6 = *(_QWORD *)(qword_141B60180 + 128);
  v7 = *(_QWORD **)v6;
  v8 = *(_QWORD **)(v6 + 8);
  if ( *(_QWORD **)v6 != v8 )
  {
    v30 = *(_QWORD **)(v6 + 8);
    while ( 1 )
    {
      v10 = (_DWORD *)*v7;
      if ( *v7 != 0 )
      {
        v11 = qword_141B5FDB8;
        if ( v10[8] != v31 || v10[9] != v32 )
        {
          v12 = (*(__int64 (__fastcall **)(__int64, _DWORD *))(*(_QWORD *)qword_141B5FDB8 + 32LL))(
                  qword_141B5FDB8,
                  v10 + 8);
          if ( v12 != (*(__int64 (__fastcall **)(__int64, int *))(*(_QWORD *)v11 + 32LL))(v11, &v31) )
          {
            v13 = qword_141B5FDB8;
            if ( v10[10] != v31 || v10[11] != v32 )
            {
              v14 = (*(__int64 (__fastcall **)(__int64, _DWORD *))(*(_QWORD *)qword_141B5FDB8 + 32LL))(
                      qword_141B5FDB8,
                      v10 + 10);
              if ( v14 != (*(__int64 (__fastcall **)(__int64, int *))(*(_QWORD *)v13 + 32LL))(v13, &v31) )
                goto LABEL_10;
            }
          }
        }
        v9 = (_QWORD *)a1[1];
        if ( v9 == (_QWORD *)a1[2] )
          break;
        *v9 = v10;
        a1[1] += 8;
      }
LABEL_10:
      if ( ++v7 == v8 )
        return a1;
    }
    v15 = a1;
    v16 = (__int64)v9 - *a1;
    v17 = (unsigned __int64)(v16 >> 3) >> 1;
    v18 = 0x1FFFFFFFFFFFFFFFLL - v17;
    v19 = (v16 >> 3) + v17;
    v29 = (v16 >> 3) + 1;
    if ( v19 <= v29 )
      v19 = (v16 >> 3) + 1;
    if ( v16 >> 3 > v18 )
      v19 = 0x1FFFFFFFFFFFFFFFLL;
    v20 = sub_1407E4490(qword_141ABD470, 8 * v19);
    *(_QWORD *)(v20 + v16) = v10;
    v21 = (_QWORD *)v15[1];
    sub_141758A00();
    if ( v21 != v9 )
      sub_141758A00();
    v22 = v20;
    v23 = *v15;
    a1 = v15;
    if ( *v15 == 0 )
    {
LABEL_36:
      *v15 = v22;
      v15[1] = v22 + 8 * v29;
      v15[2] = v22 + 8 * v19;
      v8 = v30;
      goto LABEL_10;
    }
    v24 = v15[2] - v23;
    if ( v24 == -1 )
    {
      v24 = *(unsigned int *)(v23 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_35:
        MEMORY[0x141948990](v23 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_36;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_35;
    }
    v25 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v25) >> 3 > v24 )
    {
      v26 = *(_QWORD *)(v25 + 8 * v24);
      if ( v26 != 0 )
      {
        MEMORY[0x1419475D8](v26 + 32, v23 - *(unsigned int *)(v26 + 120));
        if ( (*(_BYTE *)(v26 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v26 + 64)) == 0)
          && *(_BYTE *)(v26 + 97) != 0 )
        {
          sub_1412D33C0(v26);
        }
        goto LABEL_36;
      }
    }
    goto LABEL_35;
  }
  return a1;
}
