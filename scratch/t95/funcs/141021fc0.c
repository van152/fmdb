bool __fastcall sub_141021FC0(__int64 a1, _QWORD *a2, __int64 *a3)
{
  _QWORD *v3; // rdi
  __int64 v4; // rax
  __int64 v6; // rsi
  int v7; // eax
  _QWORD *v8; // rcx
  int v9; // eax
  __int64 *v10; // rcx
  __int64 v11; // rax
  __int64 v12; // rcx
  __int64 *v13; // rdx
  _QWORD *v14; // r15
  __int64 v15; // rax
  unsigned __int64 v16; // rax
  __int64 v17; // rdi
  __int64 v18; // rbx
  _QWORD *v19; // rdx
  __int64 *v20; // r14
  __int64 v21; // rax
  __int64 v22; // rcx
  __int64 *v23; // rsi
  __int64 v24; // rax
  __int64 v25; // rax
  __int64 v26; // rcx
  __int64 *v27; // rdx
  __int64 v28; // rax
  _QWORD *v29; // rsi
  _QWORD *v30; // r13
  __int64 v31; // r12
  __int64 *v32; // rdi
  __int64 v33; // rcx
  __int64 v34; // rax
  __int64 v35; // rcx
  int v37; // [rsp+20h] [rbp-60h] BYREF
  __int64 v38; // [rsp+28h] [rbp-58h] BYREF
  _QWORD v39[3]; // [rsp+38h] [rbp-48h] BYREF
  _QWORD v40[2]; // [rsp+50h] [rbp-30h] BYREF
  __int64 v41; // [rsp+60h] [rbp-20h]
  __int64 v42; // [rsp+68h] [rbp-18h]
  __int64 *v43; // [rsp+70h] [rbp-10h]
  __int64 v44; // [rsp+78h] [rbp-8h]
  _QWORD v45[2]; // [rsp+80h] [rbp+0h] BYREF
  _QWORD *v46; // [rsp+90h] [rbp+10h]
  __int64 v47; // [rsp+98h] [rbp+18h] BYREF
  _QWORD v48[10]; // [rsp+A0h] [rbp+20h] BYREF

  v48[2] = -2;
  v3 = a2;
  v4 = *(_QWORD *)(a1 + 816);
  if ( a2 != nullptr && v4 != 0 )
  {
    v6 = a1;
    v44 = *(_QWORD *)(a1 + 816);
    v7 = (*(__int64 (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2);
    v8 = v3;
    if ( v7 == 24 )
    {
      v9 = (*(__int64 (__fastcall **)(_QWORD *))(*v3 + 56LL))(v3);
      v8 = v3;
      if ( v9 == 24 )
      {
        v8 = v3;
        if ( (_BYTE)word_141B60320 != 0 )
          v8 = (_QWORD *)v3[6];
      }
    }
    (*(void (__fastcall **)(_QWORD *, int *))(*v8 + 144LL))(v8, &v37);
    sub_140FEAD00(&v37, v45);
    sub_1407C9510(v39);
    v10 = *(__int64 **)(v6 + 816);
    v11 = *v10;
    v12 = v10[1];
    v46 = v3;
    v43 = a3;
    if ( v11 == v12 )
      goto LABEL_14;
    v13 = nullptr;
    while ( *(_DWORD *)v11 != 1852798067 )
    {
      v11 += 16;
      if ( v11 == v12 )
        goto LABEL_15;
    }
    if ( v11 == v12 )
LABEL_14:
      v13 = nullptr;
    else
      v13 = *(__int64 **)(v11 + 8);
LABEL_15:
    if ( v13 == nullptr )
      v13 = &qword_141B5A4A0;
    v14 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v13 + 184LL))(*v13, v13, 0);
    v15 = v14[1] - *v14;
    if ( v15 != 0 )
    {
      v16 = v15 >> 3;
      v17 = 1;
      if ( v16 >= 2 )
        v17 = v16;
      v18 = 0;
      v41 = v6;
      v42 = v17;
      do
      {
        v19 = *(_QWORD **)(*v14 + 8 * v18);
        if ( v19 == nullptr )
          goto LABEL_21;
        v20 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)*v19 + 176LL))(*v19, v19, 0);
        if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64, __int64 *))(*(_QWORD *)qword_141B5EF38 + 120LL))(
               qword_141B5EF38,
               v6,
               v20) == 0 )
          goto LABEL_21;
        v21 = *v20;
        v22 = v20[1];
        if ( *v20 == v22 )
          goto LABEL_30;
        while ( *(_DWORD *)v21 != 1685218662 )
        {
          v21 += 16;
          if ( v21 == v22 )
            goto LABEL_30;
        }
        if ( v21 == v22 )
LABEL_30:
          v23 = nullptr;
        else
          v23 = *(__int64 **)(v21 + 8);
        v24 = sub_14083D4F0(v22);
        if ( v23 == nullptr )
          v23 = &qword_141B5A4A0;
        v48[1] = 0;
        v48[0] = v24 + 8;
        sub_140FEB270(&v47, v23);
        if ( (unsigned __int8)sub_140FEB670(&v47, &v37) == 0 )
        {
          v25 = *v20;
          v26 = v20[1];
          if ( *v20 == v26 )
            goto LABEL_40;
          while ( *(_DWORD *)v25 != 1819175795 )
          {
            v25 += 16;
            if ( v25 == v26 )
              goto LABEL_40;
          }
          if ( v25 == v26 )
LABEL_40:
            v27 = nullptr;
          else
            v27 = *(__int64 **)(v25 + 8);
          if ( v27 == nullptr )
            v27 = &qword_141B5A4A0;
          v28 = (*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v27 + 184LL))(*v27, v27, 0);
          v29 = *(_QWORD **)v28;
          v30 = *(_QWORD **)(v28 + 8);
          if ( *(_QWORD **)v28 == v30 )
            goto LABEL_52;
          v31 = v28;
          do
          {
            if ( *v29 != 0
              && (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v45[0]
                                                                     + 8LL * (v45[0] != *(_QWORD *)*v29)
                                                                     + 32))(
                   v45[0],
                   v45) != 0 )
            {
              if ( v29 != *(_QWORD **)(v31 + 8) )
                goto LABEL_51;
              goto LABEL_52;
            }
            ++v29;
          }
          while ( v29 != v30 );
          if ( v30 == *(_QWORD **)(v31 + 8) )
            goto LABEL_52;
        }
LABEL_51:
        sub_14083DC80(v40, v20);
        sub_14083B5F0(v39, v40);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v40[0] + 16LL))(v40[0], v40);
LABEL_52:
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v48[0] + 16LL))(v48[0], v48);
        v6 = v41;
        v17 = v42;
LABEL_21:
        ++v18;
      }
      while ( v18 != v17 );
    }
    sub_14083DB80(&v47, v39);
    v32 = v43;
    v33 = *v43;
    if ( &v47 != v43 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v33 + 16LL))(v33, v43);
      v34 = v47;
      v35 = v48[0];
      v32[1] = v48[0];
      *v32 = v34;
      v33 = sub_14083D4F0(v35) + 8;
      v48[0] = 0;
      v47 = v33;
    }
    v3 = v46;
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v33 + 16LL))(v33, &v47);
    sub_14083B0A0(v39);
    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v45[0] + 16LL))(v45[0], v45);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v38 + 16LL))(v38, &v38);
    v4 = v44;
  }
  return v3 != nullptr && v4 != 0;
}
