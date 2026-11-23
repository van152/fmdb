char __fastcall sub_1411EF390(__int64 a1, __int64 *a2, unsigned int a3, unsigned int a4)
{
  char **v8; // rcx
  char **v9; // r12
  __int64 v10; // rdx
  unsigned __int64 v11; // rbx
  __int64 v12; // r13
  unsigned __int64 v13; // rax
  __int64 v14; // r15
  __int64 v15; // r14
  __int64 v16; // rsi
  unsigned __int64 v17; // rcx
  __int64 v18; // r8
  __int64 v19; // rcx
  __int64 v20; // rsi
  __int64 v21; // rcx
  char **v22; // r14
  char *v23; // r15
  __int64 *v24; // r13
  int v25; // edi
  __int64 v26; // rcx
  __int64 v27; // rax
  __int64 v28; // rax
  unsigned __int64 v29; // rcx
  __int64 v30; // rdx
  __int64 v31; // rsi
  signed __int32 v32; // et0
  _QWORD v34[2]; // [rsp+28h] [rbp-58h] BYREF
  int v35; // [rsp+38h] [rbp-48h] BYREF
  _QWORD v36[2]; // [rsp+40h] [rbp-40h] BYREF
  __int128 v37; // [rsp+50h] [rbp-30h] BYREF
  __int64 v38; // [rsp+60h] [rbp-20h]
  __int64 v39; // [rsp+70h] [rbp-10h]
  __int64 v40; // [rsp+78h] [rbp-8h] BYREF
  __int64 v41; // [rsp+80h] [rbp+0h]
  char **v42; // [rsp+88h] [rbp+8h]
  __int64 v43; // [rsp+90h] [rbp+10h]

  v43 = -2;
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
  v37 = 0;
  v38 = 0;
  sub_1411EEAF0(a1, &v37, a3, a4);
  v9 = *((char ***)&v37 + 1);
  v8 = (char **)v37;
  v10 = *((_QWORD *)&v37 + 1) - v37;
  v11 = (__int64)(*((_QWORD *)&v37 + 1) - v37) >> 3;
  v12 = *a2;
  v13 = (a2[2] - *a2) >> 3;
  v42 = (char **)v37;
  if ( v13 < v11 )
  {
    if ( v10 < 0 )
      sub_1400526C0(v37);
    v14 = a2[1];
    v15 = sub_1407E4490(qword_141ABD470, v10);
    sub_141758A00();
    v16 = *a2;
    if ( *a2 == 0 )
      goto LABEL_17;
    v17 = a2[2] - v16;
    if ( v17 == -1 )
    {
      v17 = *(unsigned int *)(v16 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_16;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_16;
    }
    v18 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v18) >> 3 > v17 )
    {
      v19 = *(_QWORD *)(v18 + 8 * v17);
      if ( v19 != 0 )
      {
        v20 = v16 - *(unsigned int *)(v19 + 120);
        v39 = v19;
        MEMORY[0x1419475D8](v19 + 32, v20);
        v21 = v39;
        if ( (*(_BYTE *)(v39 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v39 + 64)) == 0)
          && *(_BYTE *)(v21 + 97) != 0 )
        {
          sub_1412D33C0(v21);
        }
        goto LABEL_17;
      }
    }
LABEL_16:
    MEMORY[0x141948990](v16 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_17:
    *a2 = v15;
    a2[1] = v15 + v14 - v12;
    v13 = v15 + 8 * v11;
    a2[2] = v13;
    v8 = v42;
  }
  if ( v8 != v9 )
  {
    v22 = v42;
    do
    {
      v23 = *v22;
      LOBYTE(v13) = (*v22)[10] - 3;
      if ( (unsigned __int8)v13 >= 0xFEu && *(_QWORD *)v23 != 0 )
      {
        v24 = a2;
        (*(void (__fastcall **)(_QWORD, int *))(**(_QWORD **)v23 + 144LL))(*(_QWORD *)v23, &v35);
        v25 = v23[8];
        v27 = sub_14083D4F0(v26);
        LODWORD(v41) = v25;
        v40 = v27 + 40;
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v36[0] + 16LL))(v36[0], v36);
        v36[1] = v41;
        v36[0] = v40;
        v28 = sub_14083D4F0(v41);
        v41 = 0;
        v40 = v28 + 8;
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)(v28 + 8) + 16LL))(v28 + 8, &v40);
        a2 = v24;
        sub_140FEAD00(&v35, v34);
        sub_14083B5F0(v24, v34);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v34[0] + 16LL))(v34[0], v34);
        LOBYTE(v13) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v36[0] + 16LL))(v36[0], v36);
      }
      ++v22;
    }
    while ( v22 != v9 );
  }
  if ( v42 != nullptr )
  {
    v29 = v38 - (_QWORD)v42;
    if ( v38 - (_QWORD)v42 == -1 )
    {
      v29 = *(unsigned int *)((char *)v42 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_34:
        LOBYTE(v13) = MEMORY[0x141948990]((char *)v42 - *(unsigned int *)(qword_141ABD470 + 48));
        return v13;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_34;
    }
    v30 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v30) >> 3 <= v29 )
      goto LABEL_34;
    v31 = *(_QWORD *)(v30 + 8 * v29);
    if ( v31 == 0 )
      goto LABEL_34;
    MEMORY[0x1419475D8](v31 + 32, (char *)v42 - *(unsigned int *)(v31 + 120));
    if ( *(_BYTE *)(v31 + 72) != 0 )
    {
      v32 = _InterlockedDecrement((volatile signed __int32 *)(v31 + 64));
      LOBYTE(v13) = v32 != 0;
      if ( v32 != 0 )
        return v13;
    }
    else
    {
      LOBYTE(v13) = 0;
    }
    if ( *(_BYTE *)(v31 + 97) != 0 )
      LOBYTE(v13) = sub_1412D33C0(v31);
  }
  return v13;
}
