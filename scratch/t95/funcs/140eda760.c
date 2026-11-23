char __fastcall sub_140EDA760(__int64 a1, __int64 a2, char a3)
{
  __int64 v4; // rcx
  int v5; // r9d
  __int64 v6; // rax
  __int64 v7; // rdi
  __int64 v8; // rax
  __int64 v9; // rax
  __int64 v10; // rax
  int v11; // esi
  __int64 **v12; // rax
  __int64 *v13; // rbx
  __int64 *v14; // r12
  _QWORD *v15; // r13
  __int64 v16; // r14
  unsigned int v17; // eax
  int v18; // ecx
  __int64 v19; // r15
  __int64 v20; // r13
  unsigned __int64 v21; // rsi
  unsigned __int64 v22; // rcx
  unsigned __int64 v23; // rsi
  __int64 v24; // rax
  __int64 v25; // r14
  __int64 v26; // rcx
  __int64 v27; // r15
  __int64 v28; // rbx
  unsigned __int64 v29; // rsi
  char result; // al
  __int64 v31; // rcx
  __int64 v32; // r14
  __int64 i; // r15
  _DWORD *v34; // rdi
  __int64 v35; // rbx
  int v36; // r13d
  int v37; // edi
  int v38; // eax
  int v39; // r13d
  unsigned __int64 v40; // rdi
  __int64 v41; // rcx
  __int64 v42; // rsi
  signed __int32 v43; // et0
  __int64 (__fastcall ***v44)(_QWORD, __int64); // rcx
  _QWORD v46[2]; // [rsp+30h] [rbp-50h] BYREF
  int v47; // [rsp+44h] [rbp-3Ch]
  __int64 v48; // [rsp+48h] [rbp-38h] BYREF
  _QWORD v49[2]; // [rsp+50h] [rbp-30h] BYREF
  __int64 v50; // [rsp+60h] [rbp-20h]
  unsigned __int64 v51; // [rsp+68h] [rbp-18h]
  __int64 v52; // [rsp+70h] [rbp-10h]
  char v53; // [rsp+7Eh] [rbp-2h] BYREF
  char v54; // [rsp+7Fh] [rbp-1h]
  __int64 v55; // [rsp+80h] [rbp+0h]

  v55 = -2;
  v50 = a1;
  if ( sub_140FE35F0() != 0 )
  {
    v49[0] = 0;
    v48 = sub_14083D4F0(v4) + 8;
    v6 = sub_140FE35F0();
    if ( a3 != 0 )
    {
      if ( v6 != 0 )
        (*(void (__fastcall **)(__int64, __int64, __int64 *, _QWORD))(*(_QWORD *)qword_141B5EF38 + 160LL))(
          qword_141B5EF38,
          v6,
          &v48,
          *(unsigned int *)(v50 + 12));
    }
    else if ( v6 != 0 )
    {
      (*(void (__fastcall **)(__int64, __int64, __int64 *, _QWORD))(*(_QWORD *)qword_141B5EF38 + 176LL))(
        qword_141B5EF38,
        v6,
        &v48,
        *(unsigned int *)(v50 + 12));
    }
    v8 = (*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)v48 + 176LL))(v48, &v48, 0);
    v9 = sub_1407E90B0(v8, 0);
    v10 = sub_141758910(v9, 0, (__int64)&unk_141A7E140, (__int64)&unk_141A7FB50, 0);
    v7 = v10;
    if ( v10 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v10 + 16));
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v48 + 16LL))(v48, &v48);
  }
  else
  {
    v7 = 0;
  }
  v11 = *(_DWORD *)(v50 + 12);
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
  v12 = *(__int64 ***)(qword_141B5FDC0 + 128);
  v13 = *v12;
  v14 = v12[1];
  if ( *v12 != v14 )
  {
    v52 = 0;
    v15 = nullptr;
    v51 = 0;
    v54 = a3;
    v47 = v11;
    while ( 1 )
    {
      v16 = *v13;
      if ( *v13 == 0 )
        goto LABEL_18;
      LOBYTE(v5) = v11 == 7;
      v53 = 0;
      v46[0] = 0x14175EE20LL;
      if ( (unsigned __int8)sub_1408B4E50(v16, 0, v50, v5, 1) == 0 )
        goto LABEL_18;
      if ( v7 != 0 )
      {
        v48 = 0x14187E8C8LL;
        v49[0] = v16;
        if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *, _QWORD *, char *))(*(_QWORD *)v7 + 56LL))(
               v7,
               &v48,
               v46,
               &v53) == 0 )
          goto LABEL_18;
      }
      if ( *(_QWORD *)(v16 + 96) != 0
        && (v17 = *(unsigned __int8 *)(v16 + 244)) <= 0xE
        && (v18 = 16387, _bittest(&v18, v17)) )
      {
        if ( a3 == 0 )
          goto LABEL_18;
      }
      else if ( a3 != 0 )
      {
        goto LABEL_18;
      }
      if ( v11 != 7 && *(__int16 *)(v16 + 390) < 0 )
        goto LABEL_18;
      if ( v15 == (_QWORD *)v51 )
      {
        v19 = v52;
        v20 = (__int64)v15 - v52;
        v21 = (unsigned __int64)(v20 >> 3) >> 1;
        v22 = 0x1FFFFFFFFFFFFFFFLL - v21;
        v23 = (v20 >> 3) + v21;
        v51 = (v20 >> 3) + 1;
        if ( v23 <= v51 )
          v23 = (v20 >> 3) + 1;
        if ( v20 >> 3 > v22 )
          v23 = 0x1FFFFFFFFFFFFFFFLL;
        v24 = sub_1407E4490(qword_141ABD470, 8 * v23);
        *(_QWORD *)(v24 + v20) = v16;
        v25 = v24;
        sub_141758A00();
        if ( v19 != 0 )
        {
          if ( v20 == -1 )
          {
            v20 = *(unsigned int *)(v52 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
              goto LABEL_46;
          }
          else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
          {
            goto LABEL_46;
          }
          v26 = *(_QWORD *)(qword_141ABD470 + 24);
          if ( (*(_QWORD *)(qword_141ABD470 + 32) - v26) >> 3 > (unsigned __int64)v20
            && (v27 = *(_QWORD *)(v26 + 8 * v20)) != 0 )
          {
            MEMORY[0x1419475D8](v27 + 32, v52 - *(unsigned int *)(v27 + 120));
            if ( (*(_BYTE *)(v27 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v27 + 64)) == 0)
              && *(_BYTE *)(v27 + 97) != 0 )
            {
              sub_1412D33C0(v27);
            }
          }
          else
          {
LABEL_46:
            MEMORY[0x141948990](v52 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        v15 = (_QWORD *)(v25 + 8 * v51);
        v51 = v25 + 8 * v23;
        v52 = v25;
        a3 = v54;
        v11 = v47;
        goto LABEL_18;
      }
      *v15++ = v16;
LABEL_18:
      if ( ++v13 == v14 )
        goto LABEL_51;
    }
  }
  v51 = 0;
  v15 = nullptr;
  v52 = 0;
LABEL_51:
  v50 = v7;
  v28 = v52;
  v29 = ((__int64)v15 - v52) >> 3;
  result = sub_1408B7260(v52, v15, v29);
  v32 = 500;
  if ( v29 < 0x1F4 )
    v32 = v29;
  if ( v32 != 0 )
  {
    for ( i = 0; i != v32; ++i )
    {
      v34 = *(_DWORD **)(v28 + 8 * i);
      if ( v34 != nullptr )
      {
        v35 = sub_14083D4F0(v31) + 8;
        v46[1] = 0;
        v46[0] = v35;
        v36 = v34[2];
        v37 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v34 + 56LL))(v34);
        (*(void (__fastcall **)(__int64, _QWORD *, _QWORD *))(*(_QWORD *)v35 + 24LL))(v35, v46, v49);
        v38 = v36 & v37;
        v39 = (v37 << 24) | v36 & 0x7FFFFF;
        if ( v38 == -1 )
          v39 = -8388609;
        LODWORD(v48) = v39;
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v46[0] + 16LL))(v46[0], v46);
        sub_140FEAD00((int *)&v48, v46);
        sub_14083B5F0(a2, v46);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v46[0] + 16LL))(v46[0], v46);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v49[0] + 16LL))(v49[0], v49);
        v28 = v52;
      }
    }
  }
  else if ( v28 == 0 )
  {
    goto LABEL_71;
  }
  v40 = v51 - v28;
  if ( v51 - v28 == -1 )
  {
    v40 = *(unsigned int *)(v28 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
LABEL_70:
      result = MEMORY[0x141948990](v28 - *(unsigned int *)(qword_141ABD470 + 48));
      goto LABEL_71;
    }
  }
  else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
  {
    goto LABEL_70;
  }
  v41 = *(_QWORD *)(qword_141ABD470 + 24);
  if ( (*(_QWORD *)(qword_141ABD470 + 32) - v41) >> 3 <= v40 )
    goto LABEL_70;
  v42 = *(_QWORD *)(v41 + 8 * v40);
  if ( v42 == 0 )
    goto LABEL_70;
  MEMORY[0x1419475D8](v42 + 32, v28 - *(unsigned int *)(v42 + 120));
  if ( *(_BYTE *)(v42 + 72) != 0 )
  {
    v43 = _InterlockedDecrement((volatile signed __int32 *)(v42 + 64));
    result = v43 != 0;
    if ( v43 != 0 )
      goto LABEL_71;
  }
  else
  {
    result = 0;
  }
  if ( *(_BYTE *)(v42 + 97) != 0 )
    result = sub_1412D33C0(v42);
LABEL_71:
  v44 = (__int64 (__fastcall ***)(_QWORD, __int64))v50;
  if ( v50 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v50 + 16)) == 0 )
    return (**v44)(v44, 1);
  return result;
}
