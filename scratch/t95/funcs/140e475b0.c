__int64 __fastcall sub_140E475B0(__int64 *a1, _BYTE *a2)
{
  __int64 v4; // rax
  __int64 v5; // rcx
  __int64 *v6; // rdx
  __int64 *v7; // r14
  int v8; // edi
  __int64 v9; // rax
  __int64 v10; // rcx
  __int64 *v11; // rdx
  int v12; // r13d
  __int64 v13; // rbx
  __int64 v14; // rax
  __int64 v15; // rcx
  __int64 v16; // rdx
  __int64 *v17; // rdx
  int v18; // ebx
  __int64 v19; // rdx
  bool v20; // si
  int v21; // r15d
  __int64 v22; // rax
  __int64 *v23; // rbx
  unsigned int v24; // r13d
  char v25; // si
  __int64 *v26; // rdx
  int v27; // r15d
  int v28; // ecx
  unsigned int v29; // eax
  __int64 v30; // rax
  __int64 v31; // rax
  _DWORD *v32; // rbx
  int v33; // eax
  __int64 v34; // rax
  __int64 *v35; // rdx
  __int64 v36; // rcx
  __int64 *v37; // rax
  __int64 v38; // rax
  __int64 v39; // rax
  __int64 v40; // rax
  __int64 v41; // rcx
  __int64 v42; // rcx
  __int64 v43; // rsi
  unsigned __int64 v44; // rsi
  __int64 v45; // rax
  unsigned int v47; // eax
  __int64 v48; // rcx
  __int64 v49; // rsi
  __int64 v50; // rsi
  __int64 v51; // rax
  __int64 v52; // rcx
  int v53; // esi
  __int64 v54; // rax
  int v55; // [rsp+38h] [rbp-38h]
  int v56; // [rsp+40h] [rbp-30h]
  __int64 v57; // [rsp+48h] [rbp-28h]
  unsigned __int64 v58; // [rsp+50h] [rbp-20h] BYREF
  unsigned __int64 v59; // [rsp+58h] [rbp-18h]
  unsigned __int64 v60; // [rsp+60h] [rbp-10h]
  _QWORD v61[9]; // [rsp+68h] [rbp-8h] BYREF

  v61[1] = -2;
  v4 = *a1;
  v5 = a1[1];
  v6 = nullptr;
  if ( v4 != v5 )
  {
    while ( *(_DWORD *)v4 != 1685353593 )
    {
      v4 += 16;
      if ( v4 == v5 )
        goto LABEL_8;
    }
    if ( v4 == v5 )
      v6 = nullptr;
    else
      v6 = *(__int64 **)(v4 + 8);
  }
LABEL_8:
  v7 = &qword_141B5A4A0;
  if ( v6 == nullptr )
    v6 = &qword_141B5A4A0;
  v8 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v6 + 64LL))(*v6);
  v9 = *a1;
  v10 = a1[1];
  v11 = nullptr;
  if ( *a1 != v10 )
  {
    while ( *(_DWORD *)v9 != 1684239481 )
    {
      v9 += 16;
      if ( v9 == v10 )
        goto LABEL_17;
    }
    if ( v9 == v10 )
      v11 = nullptr;
    else
      v11 = *(__int64 **)(v9 + 8);
  }
LABEL_17:
  if ( v11 == nullptr )
    v11 = &qword_141B5A4A0;
  v12 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v11 + 64LL))(*v11);
  if ( a2 != nullptr )
    *a2 = 0;
  v13 = 0;
  switch ( v8 )
  {
    case 1:
      if ( (_BYTE)word_141B60320 != 0
        && *(_QWORD *)(*(_QWORD *)(qword_141B5FE10 + 128) + 8LL) != **(_QWORD **)(qword_141B5FE10 + 128) )
      {
        goto LABEL_26;
      }
      return 0;
    case 5:
    case 9:
      return v13;
    case 6:
      if ( *(_QWORD *)(*(_QWORD *)(qword_141B5FDE8 + 128) + 8LL) - **(_QWORD **)(qword_141B5FDE8 + 128) <= 0x638u )
        goto LABEL_26;
      return 0;
    default:
LABEL_26:
      v14 = *a1;
      v15 = a1[1];
      if ( *a1 == v15 )
        goto LABEL_37;
      v16 = *a1;
      break;
  }
  while ( *(_DWORD *)v16 != 1685417577 )
  {
    v16 += 16;
    if ( v16 == v15 )
      goto LABEL_37;
  }
  if ( v16 == v15 || *(_QWORD *)(v16 + 8) == 0 )
  {
LABEL_37:
    v61[0] = 0xFFFFFFFFLL;
    v60 = 0;
    v18 = -1;
    if ( v14 == v15 )
      goto LABEL_50;
    goto LABEL_38;
  }
  v17 = nullptr;
  while ( *(_DWORD *)v14 != 1685417577 )
  {
    v14 += 16;
    if ( v14 == v15 )
      goto LABEL_47;
  }
  if ( v14 == v15 )
    v17 = nullptr;
  else
    v17 = *(__int64 **)(v14 + 8);
LABEL_47:
  if ( v17 == nullptr )
    v17 = &qword_141B5A4A0;
  sub_140FE3720(&v58, v17);
  v18 = v58;
  v61[0] = v58;
  v14 = *a1;
  v15 = a1[1];
  v60 = HIDWORD(v58);
  if ( v14 != v15 )
  {
LABEL_38:
    v19 = v14;
    while ( *(_DWORD *)v19 != 1853322601 )
    {
      v19 += 16;
      if ( v19 == v15 )
        goto LABEL_50;
    }
    if ( v19 != v15 )
    {
      v20 = *(_QWORD *)(v19 + 8) != 0;
      goto LABEL_51;
    }
  }
LABEL_50:
  v20 = false;
LABEL_51:
  v56 = v12;
  v57 = (__int64)a2;
  if ( (_BYTE)word_141B60320 == 0 )
  {
    if ( v20 )
      goto LABEL_66;
    v24 = -1;
    v25 = 0;
LABEL_71:
    v27 = v8;
    v28 = v60;
LABEL_113:
    v39 = sub_140F49070((unsigned int)&qword_141B5FDA8, v27, v56, v18, v28, v24, v57);
    if ( v39 != 0 )
    {
      v13 = v39;
      if ( v25 == 0 )
      {
        v40 = *a1;
        v41 = a1[1];
        if ( *a1 == v41 )
          goto LABEL_118;
        while ( *(_DWORD *)v40 != 1685417577 )
        {
          v40 += 16;
          if ( v40 == v41 )
            goto LABEL_118;
        }
        if ( v40 == v41 || *(_QWORD *)(v40 + 8) == 0 )
        {
LABEL_118:
          v42 = *(unsigned int *)(v13 + 16);
          v43 = *(unsigned int *)(v13 + 12);
          if ( (_DWORD)v42 != 0 )
            v43 = (unsigned int)v42;
          v44 = *(int *)(v13 + 12) | (unsigned __int64)(v43 << 32);
          v45 = sub_14083D4F0(v42);
          v59 = v44;
          v58 = v45 + 72;
          sub_140835380(a1, 1685417577, (__int64 *)&v58);
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v58 + 16LL))(v58, &v58);
        }
        else
        {
          if ( HIDWORD(v61[0]) == 0 )
          {
            v47 = *(_DWORD *)(v13 + 16);
            v48 = *(int *)(v13 + 12);
            v49 = *(unsigned int *)(v13 + 12);
            if ( v47 != 0 )
              v49 = v47;
            HIDWORD(v61[0]) = v49;
            v50 = v48 | (v49 << 32);
            v51 = sub_14083D4F0(v48);
            v59 = v50;
            v58 = v51 + 72;
            sub_140835380(a1, 1685417577, (__int64 *)&v58);
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v58 + 16LL))(v58, &v58);
          }
          if ( LODWORD(v61[0]) != *(_DWORD *)(v13 + 12)
            && (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 32LL))(qword_141B5AD60) == 0 )
          {
            v53 = *(_DWORD *)(v13 + 12);
            v54 = sub_14083D4F0(v52);
            LODWORD(v59) = v53;
            v58 = v54 + 40;
            sub_140835380(a1, 1853322601, (__int64 *)&v58);
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)v58 + 16LL))(v58, &v58);
          }
        }
      }
      goto LABEL_121;
    }
    return 0;
  }
  v21 = v18;
  v22 = qword_141B60C30;
  v23 = nullptr;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    while ( *(_DWORD *)v22 != 1986359923 )
    {
      v22 += 16;
      if ( v22 == qword_141B60C38 )
        goto LABEL_61;
    }
    if ( v22 == qword_141B60C38 )
      v23 = nullptr;
    else
      v23 = *(__int64 **)(v22 + 8);
  }
LABEL_61:
  if ( v23 == nullptr )
    v23 = &qword_141B5A4A0;
  if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v23 + 8LL))(*v23, v23) == 0
    || (*(int (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v23 + 64LL))(*v23, v23) < 2962
    || !v20 )
  {
    v24 = -1;
    v25 = 0;
    v18 = v21;
    if ( (_BYTE)word_141B60320 != 0 )
      goto LABEL_100;
    goto LABEL_71;
  }
  v14 = *a1;
  v15 = a1[1];
  v18 = v21;
LABEL_66:
  v26 = nullptr;
  if ( v14 == v15 )
  {
LABEL_69:
    v27 = v8;
  }
  else
  {
    while ( *(_DWORD *)v14 != 1853322601 )
    {
      v14 += 16;
      if ( v14 == v15 )
        goto LABEL_69;
    }
    v27 = v8;
    if ( v14 == v15 )
      v26 = nullptr;
    else
      v26 = *(__int64 **)(v14 + 8);
  }
  if ( v26 == nullptr )
    v26 = &qword_141B5A4A0;
  v29 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v26 + 64LL))(*v26);
  v24 = v29;
  if ( (_BYTE)word_141B60320 != 0 )
  {
    v55 = v18;
    v30 = sub_140F216C0(&qword_141B5FDA8);
    v31 = (*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v30 + 40LL))(v30, v24);
    v32 = (_DWORD *)v31;
    if ( v27 == 1 && v31 != 0 )
    {
      v33 = *(_DWORD *)(v31 + 16);
      if ( v33 == 0 )
        v33 = v32[3];
      if ( v33 == (_DWORD)v60 )
      {
        v34 = qword_141B60C30;
        v35 = nullptr;
        if ( qword_141B60C30 != qword_141B60C38 )
        {
          while ( *(_DWORD *)v34 != 1314013776 )
          {
            v34 += 16;
            if ( v34 == qword_141B60C38 )
              goto LABEL_94;
          }
          if ( v34 == qword_141B60C38 )
            v35 = nullptr;
          else
            v35 = *(__int64 **)(v34 + 8);
        }
LABEL_94:
        if ( v35 == nullptr )
          v35 = &qword_141B5A4A0;
        if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v35 + 48LL))(*v35) != 0
          && (*(unsigned __int8 (__fastcall **)(_DWORD *))(*(_QWORD *)v32 + 48LL))(v32) == 17 )
        {
          goto LABEL_98;
        }
      }
    }
    else if ( v31 == 0 )
    {
LABEL_98:
      LODWORD(v61[0]) = v24;
      v25 = 1;
      v18 = v24;
LABEL_100:
      v36 = qword_141B60C30;
      v37 = nullptr;
      if ( qword_141B60C30 == qword_141B60C38 )
      {
LABEL_103:
        v27 = v8;
      }
      else
      {
        while ( *(_DWORD *)v36 != 1348554322 )
        {
          v36 += 16;
          if ( v36 == qword_141B60C38 )
            goto LABEL_103;
        }
        v27 = v8;
        if ( v36 == qword_141B60C38 )
          v37 = nullptr;
        else
          v37 = *(__int64 **)(v36 + 8);
      }
      if ( v37 != nullptr )
        v7 = v37;
      if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v7 + 48LL))(*v7, v7) != 0 )
      {
        v38 = sub_140F216C0(&qword_141B5FDA8);
        if ( (*(__int64 (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)v38 + 32LL))(v38, v61) != 0 )
          return 0;
        v18 = v61[0];
        v28 = HIDWORD(v61[0]);
      }
      else
      {
        v28 = v60;
      }
      goto LABEL_113;
    }
    v25 = 1;
    v18 = v55;
    if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 32LL))(qword_141B5AD60) == 0 )
      return 0;
    goto LABEL_100;
  }
  v13 = sub_140F49070((unsigned int)&qword_141B5FDA8, v27, v56, v18, v60, v29, v57);
  if ( v13 == 0 )
    return 0;
LABEL_121:
  if ( v27 == 3 && (_BYTE)word_141B60320 != 0 )
    sub_140F3F7E0(&qword_141B5FDA8);
  return v13;
}
