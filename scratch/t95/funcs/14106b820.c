__int64 __fastcall sub_14106B820(__int64 a1, __int64 *a2)
{
  int v4; // r14d
  __int16 v5; // r15
  __int64 *v6; // r12
  int v7; // eax
  unsigned __int64 v8; // rax
  __int64 v9; // rdx
  _QWORD *v10; // rax
  __int64 *v11; // rdx
  __int64 v12; // rcx
  __int64 v13; // rdx
  __int64 v14; // rax
  __int64 v15; // rsi
  __int64 v16; // r12
  unsigned __int64 v17; // rax
  __int64 v18; // r8
  unsigned __int64 v19; // rdx
  unsigned __int64 v20; // rax
  __int64 v21; // rdi
  unsigned __int64 v22; // rcx
  __int64 v23; // rdx
  __int64 v24; // rbx
  unsigned int v25; // eax
  unsigned int v26; // ebx
  unsigned __int64 v27; // rcx
  __int64 v28; // rdi
  __int64 v29; // rdi
  unsigned __int64 v31; // [rsp+28h] [rbp-48h]
  __int64 *v32; // [rsp+30h] [rbp-40h]
  __int64 v33; // [rsp+38h] [rbp-38h]
  __int64 *v34; // [rsp+48h] [rbp-28h]
  __int128 v35; // [rsp+50h] [rbp-20h] BYREF
  __int64 *v36; // [rsp+60h] [rbp-10h]
  __int64 v37; // [rsp+70h] [rbp+0h]

  v37 = -2;
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
  v35 = 0;
  v36 = nullptr;
  v4 = (unsigned __int16)((unsigned int)(*(_DWORD *)(a1 + 1240) - *(_DWORD *)(a1 + 1232)) >> 2);
  if ( (unsigned __int16)((unsigned int)(*(_DWORD *)(a1 + 1240) - *(_DWORD *)(a1 + 1232)) >> 2) != 0 )
  {
    v5 = 1;
    v6 = nullptr;
    v34 = a2;
    do
    {
      v8 = *(unsigned int *)(*(_QWORD *)(a1 + 1232) + 4LL * (__int16)(v5 - 1));
      if ( (v8 & 0x80000000) != 0LL || qword_141B5FE10 == 0 )
        goto LABEL_7;
      if ( (_BYTE)word_141B60320 != 0
        || (v9 = *(_QWORD *)(qword_141B5FE10 + 96), (*(_QWORD *)(qword_141B5FE10 + 104) - v9) >> 3 <= v8) )
      {
        v11 = *(__int64 **)(qword_141B5FE10 + 128);
        v12 = *v11;
        v13 = v11[1] - *v11;
        if ( v13 == 0 || v13 >> 3 <= (unsigned __int64)(unsigned int)v8 )
          goto LABEL_7;
        v10 = (_QWORD *)(v12 + 8LL * (unsigned int)v8);
      }
      else
      {
        v10 = (_QWORD *)(v9 + 8 * v8);
      }
      if ( *v10 != 0 )
      {
        v14 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*v10 + 1672LL))(*v10);
        if ( v14 != 0 )
        {
          v15 = v14;
          if ( v6 == v36 )
          {
            v32 = v6;
            v16 = (__int64)v6 - v35;
            v17 = (unsigned __int64)(v16 >> 3) >> 1;
            v18 = 0x1FFFFFFFFFFFFFFFLL;
            v19 = 0x1FFFFFFFFFFFFFFFLL - v17;
            v20 = (v16 >> 3) + v17;
            v31 = (v16 >> 3) + 1;
            if ( v20 <= v31 )
              v20 = (v16 >> 3) + 1;
            if ( v16 >> 3 <= v19 )
              v18 = v20;
            v33 = v18;
            v21 = sub_1407E4490(qword_141ABD470, 8 * v18);
            *(_QWORD *)(v21 + v16) = v15;
            sub_141758A00();
            if ( *((_QWORD *)&v35 + 1) != (_QWORD)v32 )
              sub_141758A00();
            if ( (_QWORD)v35 != 0 )
            {
              v22 = (unsigned __int64)v36 - v35;
              if ( (__int64 *)((char *)v36 - v35) == (__int64 *)-1LL )
              {
                v22 = *(unsigned int *)(v35 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                  goto LABEL_35;
              }
              else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
              {
                goto LABEL_35;
              }
              v23 = *(_QWORD *)(qword_141ABD470 + 24);
              if ( (*(_QWORD *)(qword_141ABD470 + 32) - v23) >> 3 > v22 && (v24 = *(_QWORD *)(v23 + 8 * v22)) != 0 )
              {
                MEMORY[0x1419475D8](v24 + 32, v35 - *(unsigned int *)(v24 + 120));
                if ( (*(_BYTE *)(v24 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v24 + 64)) == 0)
                  && *(_BYTE *)(v24 + 97) != 0 )
                {
                  sub_1412D33C0(v24);
                }
              }
              else
              {
LABEL_35:
                MEMORY[0x141948990](v35 - *(unsigned int *)(qword_141ABD470 + 48));
              }
            }
            *(_QWORD *)&v35 = v21;
            v6 = (__int64 *)(v21 + 8 * v31);
            *((_QWORD *)&v35 + 1) = v6;
            v36 = (__int64 *)(v21 + 8 * v33);
            a2 = v34;
            goto LABEL_7;
          }
          *v6 = v14;
          v6 = (__int64 *)(*((_QWORD *)&v35 + 1) + 8LL);
          *((_QWORD *)&v35 + 1) += 8LL;
        }
      }
LABEL_7:
      v7 = v5++;
    }
    while ( v4 > v7 );
  }
  LOBYTE(v25) = sub_1410C4E30((__int64 *)&v35, 0, a2);
  v26 = v25;
  if ( (_QWORD)v35 != 0 )
  {
    v27 = (unsigned __int64)v36 - v35;
    if ( (__int64 *)((char *)v36 - v35) == (__int64 *)-1LL )
    {
      v27 = *(unsigned int *)(v35 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_49:
        MEMORY[0x141948990](v35 - *(unsigned int *)(qword_141ABD470 + 48));
        return v26;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_49;
    }
    v28 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v28) >> 3 <= v27 )
      goto LABEL_49;
    v29 = *(_QWORD *)(v28 + 8 * v27);
    if ( v29 == 0 )
      goto LABEL_49;
    MEMORY[0x1419475D8](v29 + 32, v35 - *(unsigned int *)(v29 + 120));
    if ( (*(_BYTE *)(v29 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v29 + 64)) == 0)
      && *(_BYTE *)(v29 + 97) != 0 )
    {
      sub_1412D33C0(v29);
    }
  }
  return v26;
}
