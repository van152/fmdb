char __fastcall sub_140E957C0(__int64 *a1, __int64 *a2)
{
  __int64 v2; // rax
  __int64 v3; // rcx
  int *v4; // r12
  __int64 v5; // r14
  _QWORD *v6; // r13
  int **v7; // rdx
  __int64 v8; // rsi
  int *v9; // r15
  int v10; // eax
  _DWORD *v11; // r15
  int *v12; // rax
  volatile signed __int32 *v13; // rcx
  volatile signed __int32 *v14; // rsi
  int v15; // r15d
  int v16; // edi
  __int64 v17; // rbx
  unsigned int v18; // eax
  __int64 v19; // rdi
  __int64 v20; // rdi
  volatile signed __int32 *v21; // rcx
  int v22; // esi
  __int64 v23; // rbx
  __int64 v24; // rsi
  _BYTE *v25; // rdi
  unsigned int v26; // eax
  int *v27; // r15
  __int64 v28; // rcx
  int **v29; // rax
  __int64 v30; // rsi
  int *v31; // rbx
  int v32; // r13d
  _DWORD *v33; // rbx
  int *v34; // rcx
  signed __int32 v35; // eax
  volatile signed __int32 *v36; // r15
  int v37; // edi
  __int64 v38; // r12
  unsigned int v39; // eax
  __int64 v40; // rdi
  __int64 v41; // rdi
  volatile signed __int32 *v42; // rcx
  int v43; // r15d
  int v44; // edi
  __int64 v45; // rsi
  __int64 v46; // rdi
  _BYTE *v47; // rbx
  unsigned int v48; // eax
  __int64 v49; // rcx
  __int64 v50; // rax
  __int64 v51; // rcx
  __int64 v52; // rax
  __int64 v53; // rax
  __int64 v54; // rcx
  char result; // al
  __int64 v56; // rcx
  unsigned int v58; // [rsp+38h] [rbp-28h]
  __int64 v60; // [rsp+48h] [rbp-18h] BYREF
  __int64 v61; // [rsp+50h] [rbp-10h]
  _QWORD v62[9]; // [rsp+58h] [rbp-8h] BYREF

  v62[1] = -2;
  v62[0] = 0;
  v2 = *a1;
  v3 = a1[1];
  if ( v3 != v2 )
  {
    v4 = nullptr;
    v5 = 0;
    while ( 1 )
    {
      v6 = *(_QWORD **)(v2 + 8 * v5);
      if ( *v6 != 0 )
        break;
LABEL_4:
      if ( ++v5 >= (unsigned __int64)((v3 - v2) >> 3) )
        goto LABEL_79;
    }
    v7 = (int **)(*v6 + 192LL);
    if ( v4 != nullptr && (v8 = (unsigned int)*v4, *v4 != 0) )
    {
      v9 = *v7;
      if ( *v7 != nullptr )
      {
        v10 = *v9;
        v11 = v9 + 1;
        if ( v10 != -1 )
        {
          if ( v10 <= 0 )
            goto LABEL_36;
LABEL_28:
          v58 = v10;
          v16 = v10 + v8;
          v17 = sub_1412EC810(264, (unsigned int)(v10 + v8));
          *(_DWORD *)v17 = 0;
          v18 = 0;
          if ( v16 <= 0 )
            v16 = 0;
          *(_DWORD *)(v17 + 4) = v16;
          v19 = v17 + 8;
          *(_BYTE *)(v17 + 8) = 0;
          if ( (int)v8 > 0 )
          {
            sub_141758A00();
            *(_BYTE *)(v19 + v8) = 0;
            v18 = v8;
          }
          v4 = (int *)(v17 + 4);
          v20 = v18 + v19;
          sub_141758A00();
          *(_BYTE *)(v58 + v20) = 0;
          v21 = (volatile signed __int32 *)(v62[0] - 4LL);
          if ( v62[0] != 0 && _InterlockedDecrement(v21) == 0 )
            sub_1412EC9A0((__int64)v21);
          v62[0] = 0;
          _InterlockedIncrement((volatile signed __int32 *)v17);
          v62[0] = v17 + 4;
          goto LABEL_36;
        }
        v10 = sub_141758DB0(v11);
        if ( v10 > 0 )
          goto LABEL_28;
      }
    }
    else
    {
      if ( v62 != v7 )
      {
        v12 = *v7;
        v13 = v4 - 1;
        if ( v4 == nullptr )
          v13 = nullptr;
        v14 = v12 - 1;
        if ( v12 != nullptr )
        {
          if ( v4 != nullptr && _InterlockedDecrement(v13) == 0 )
            sub_1412EC9A0((__int64)v13);
          v62[0] = 0;
          _InterlockedIncrement(v14);
          v4 = (int *)(v14 + 1);
        }
        else
        {
          if ( v4 != nullptr && _InterlockedDecrement(v13) == 0 )
            sub_1412EC9A0((__int64)v13);
          v4 = nullptr;
        }
        v62[0] = v4;
      }
      if ( v4 == nullptr )
      {
        v15 = 0;
        goto LABEL_37;
      }
    }
LABEL_36:
    v15 = *v4;
LABEL_37:
    v22 = v15 + 1;
    v23 = sub_1412EC810(264, (unsigned int)(v15 + 1));
    *(_DWORD *)v23 = 0;
    if ( v15 + 1 <= 0 )
      v22 = 0;
    *(_DWORD *)(v23 + 4) = v22;
    v24 = v23 + 8;
    *(_BYTE *)(v23 + 8) = 0;
    if ( v15 <= 0 )
    {
      v26 = 0;
      v25 = (_BYTE *)(v23 + 8);
      if ( v15 != 0 )
        goto LABEL_43;
    }
    else
    {
      sub_141758A00();
      v25 = (_BYTE *)(v24 + (unsigned int)v15);
    }
    *v25 = 0;
    v26 = v15;
LABEL_43:
    v27 = (int *)(v23 + 4);
    *(_WORD *)(v24 + v26) = 32;
    if ( v62[0] != 0 )
    {
      v28 = v62[0] - 4LL;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v62[0] - 4LL)) == 0 )
        sub_1412EC9A0(v28);
    }
    v62[0] = 0;
    _InterlockedIncrement((volatile signed __int32 *)v23);
    v62[0] = v23 + 4;
    v29 = (int **)(*v6 + 200LL);
    v30 = *(unsigned int *)(v23 + 4);
    if ( *(_DWORD *)(v23 + 4) != 0 )
    {
      v31 = *v29;
      if ( *v29 != nullptr )
      {
        v32 = *v31;
        v33 = v31 + 1;
        if ( v32 != -1 )
        {
          if ( v32 <= 0 )
            goto LABEL_66;
          goto LABEL_57;
        }
        v32 = sub_141758DB0(v33);
        if ( v32 > 0 )
        {
LABEL_57:
          v37 = v32 + v30;
          v38 = sub_1412EC810(264, (unsigned int)(v32 + v30));
          *(_DWORD *)v38 = 0;
          v39 = 0;
          if ( v32 + (int)v30 <= 0 )
            v37 = 0;
          *(_DWORD *)(v38 + 4) = v37;
          v40 = v38 + 8;
          *(_BYTE *)(v38 + 8) = 0;
          if ( (int)v30 > 0 )
          {
            sub_141758A00();
            *(_BYTE *)(v40 + v30) = 0;
            v39 = v30;
          }
          v27 = (int *)(v38 + 4);
          v41 = v39 + v40;
          sub_141758A00();
          *(_BYTE *)((unsigned int)v32 + v41) = 0;
          v42 = (volatile signed __int32 *)(v62[0] - 4LL);
          if ( v62[0] != 0 && _InterlockedDecrement(v42) == 0 )
            sub_1412EC9A0((__int64)v42);
          v62[0] = 0;
          _InterlockedIncrement((volatile signed __int32 *)v38);
LABEL_65:
          v62[0] = v27;
        }
      }
    }
    else if ( v62 != v29 )
    {
      v34 = *v29;
      v35 = _InterlockedExchangeAdd((volatile signed __int32 *)v23, 0xFFFFFFFF);
      v36 = v34 - 1;
      if ( v34 == nullptr )
      {
        if ( v35 == 1 )
          sub_1412EC9A0(v23);
        v62[0] = 0;
        v43 = 0;
LABEL_67:
        v44 = v43 + 1;
        v45 = sub_1412EC810(264, (unsigned int)(v43 + 1));
        *(_DWORD *)v45 = 0;
        if ( v43 + 1 <= 0 )
          v44 = 0;
        *(_DWORD *)(v45 + 4) = v44;
        v46 = v45 + 8;
        *(_BYTE *)(v45 + 8) = 0;
        if ( v43 <= 0 )
        {
          v48 = 0;
          v47 = (_BYTE *)(v45 + 8);
          if ( v43 != 0 )
          {
LABEL_73:
            v4 = (int *)(v45 + 4);
            *(_WORD *)(v46 + v48) = 32;
            if ( v62[0] != 0 )
            {
              v49 = v62[0] - 4LL;
              if ( _InterlockedDecrement((volatile signed __int32 *)(v62[0] - 4LL)) == 0 )
                sub_1412EC9A0(v49);
            }
            v62[0] = 0;
            _InterlockedIncrement((volatile signed __int32 *)v45);
            v62[0] = v45 + 4;
            v2 = *a1;
            v3 = a1[1];
            goto LABEL_4;
          }
        }
        else
        {
          sub_141758A00();
          v47 = (_BYTE *)(v46 + (unsigned int)v43);
        }
        *v47 = 0;
        v48 = v43;
        goto LABEL_73;
      }
      if ( v35 == 1 )
        sub_1412EC9A0(v23);
      v62[0] = 0;
      _InterlockedIncrement(v36);
      v27 = (int *)(v36 + 1);
      goto LABEL_65;
    }
LABEL_66:
    v43 = *v27;
    goto LABEL_67;
  }
LABEL_79:
  v50 = sub_14083D4F0(v3);
  v61 = 0;
  v51 = v62[0];
  if ( v62[0] != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v62[0] - 4LL));
  v61 = v51;
  v52 = v50 + 136;
  v60 = v52;
  if ( &v60 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a2 + 16LL))(*a2, a2);
    v53 = v60;
    v54 = v61;
    a2[1] = v61;
    *a2 = v53;
    v52 = sub_14083D4F0(v54) + 8;
    v61 = 0;
    v60 = v52;
  }
  result = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v52 + 16LL))(v52, &v60);
  v56 = v62[0];
  if ( v62[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v62[0] - 4LL)) == 0 )
    return sub_1412EC9A0(v56 - 4);
  return result;
}
