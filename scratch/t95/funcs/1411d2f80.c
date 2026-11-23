char __fastcall sub_1411D2F80(__int64 a1, __int64 a2, __int64 a3, char a4, unsigned __int8 a5)
{
  __int64 v7; // rbp
  unsigned __int64 v8; // rbx
  __int64 v9; // rax
  __int64 v10; // rcx
  __int64 v11; // rbp
  unsigned __int64 v12; // rbx
  __int64 v13; // rax
  __int64 v14; // rcx
  __int64 v15; // rbx
  unsigned __int64 v16; // rbp
  char v17; // r12
  __int64 v18; // rax
  __int64 v19; // rax
  __int64 v20; // rax
  __int64 v21; // rbx
  unsigned __int64 v22; // rbp
  __int64 v23; // rax
  __int64 v24; // rax
  __int64 v25; // rax
  __int64 v26; // rbx
  unsigned __int64 v27; // rbp
  __int64 v28; // rax
  __int64 v29; // rax
  __int64 v30; // rax
  _QWORD *v31; // rbx
  _QWORD *v32; // rax
  _QWORD *v33; // rbp
  __int64 v34; // r14
  _QWORD *v35; // rbx
  _QWORD *v36; // rax
  _QWORD *v37; // rbp
  __int64 v38; // r14
  _QWORD *v39; // rbx
  _QWORD *v40; // rax
  _QWORD *v41; // rbp
  __int64 v42; // r14
  __int64 v43; // rbx
  __int64 v44; // rbp
  unsigned __int64 v45; // rbx
  __int64 v46; // rax
  __int64 v47; // rcx
  __int64 v48; // rdx
  __int64 v49; // rdx
  __int64 v50; // rax
  _QWORD *v51; // rax
  __int64 v52; // rbp
  __int64 v53; // rbp
  __int64 v54; // rbx
  __int64 v56; // [rsp+38h] [rbp-50h] BYREF
  __int64 v57; // [rsp+40h] [rbp-48h]

  if ( a4 != 0 )
  {
    v7 = *(_QWORD *)(a1 + 24);
    if ( *(_QWORD *)(a1 + 32) != v7 )
    {
      v8 = 0;
      do
      {
        v56 = *(_QWORD *)(v7 + 8 * v8);
        if ( (unsigned __int8)sub_140F7EE40(a3, (unsigned int)&v56, *(_QWORD *)(a3 + 152), a5, 1, 0) != 0 )
        {
          *(_QWORD *)(v7 + 8 * v8) = v56;
          v9 = *(_QWORD *)(*(_QWORD *)(a1 + 24) + 8 * v8);
          if ( v9 != 0 && *(_QWORD *)(v9 + 48) == -1 )
          {
            v10 = *(int *)(a1 + 8);
            *(_QWORD *)(v9 + 48) = v10;
            if ( v10 != 0 )
              *(_BYTE *)(v9 + 47) = *(_BYTE *)(v10 + 186) != 0;
            else
              *(_BYTE *)(v9 + 47) = -1;
            *(_BYTE *)(v9 + 47) = *(_BYTE *)(a1 + 186);
          }
        }
        ++v8;
        v7 = *(_QWORD *)(a1 + 24);
      }
      while ( v8 < (*(_QWORD *)(a1 + 32) - v7) >> 3 );
    }
    v11 = *(_QWORD *)(a1 + 48);
    if ( *(_QWORD *)(a1 + 56) != v11 )
    {
      v12 = 0;
      do
      {
        v56 = *(_QWORD *)(v11 + 8 * v12);
        if ( (unsigned __int8)sub_140F7EE40(a3, (unsigned int)&v56, *(_QWORD *)(a3 + 152), a5, 1, 0) != 0 )
        {
          *(_QWORD *)(v11 + 8 * v12) = v56;
          v13 = *(_QWORD *)(*(_QWORD *)(a1 + 48) + 8 * v12);
          if ( v13 != 0 && *(_QWORD *)(v13 + 48) == -1 )
          {
            v14 = *(int *)(a1 + 8);
            *(_QWORD *)(v13 + 48) = v14;
            if ( v14 != 0 )
              *(_BYTE *)(v13 + 47) = *(_BYTE *)(v14 + 186) != 0;
            else
              *(_BYTE *)(v13 + 47) = -1;
            *(_BYTE *)(*(_QWORD *)(*(_QWORD *)(a1 + 48) + 8 * v12) + 47LL) = *(_BYTE *)(a1 + 186);
          }
        }
        ++v12;
        v11 = *(_QWORD *)(a1 + 48);
      }
      while ( v12 < (*(_QWORD *)(a1 + 56) - v11) >> 3 );
    }
    v15 = *(_QWORD *)(a1 + 96);
    if ( *(_QWORD *)(a1 + 104) == v15 )
    {
      v17 = 0;
    }
    else
    {
      v16 = 0;
      v17 = 0;
      do
      {
        if ( (a5 & 8) != 0 )
        {
          v20 = *(_QWORD *)(v15 + 8 * v16);
          if ( v20 != 0 )
            v19 = v20 + *(int *)(*(_QWORD *)(v20 + 8) + 4LL) + 8;
          else
            v19 = 0;
        }
        else
        {
          v19 = *(_QWORD *)(v15 + 8 * v16);
        }
        v56 = v19;
        if ( (unsigned __int8)sub_140F80250(a3, &v56, a5, 0) != 0 )
        {
          if ( v56 != 0 )
            v18 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v56 + 1688LL))(v56);
          else
            v18 = 0;
          *(_QWORD *)(v15 + 8 * v16) = v18;
          v17 = 1;
        }
        ++v16;
        v15 = *(_QWORD *)(a1 + 96);
      }
      while ( v16 < (*(_QWORD *)(a1 + 104) - v15) >> 3 );
    }
    v21 = *(_QWORD *)(a1 + 120);
    if ( *(_QWORD *)(a1 + 128) != v21 )
    {
      v22 = 0;
      do
      {
        if ( (a5 & 8) != 0 )
        {
          v25 = *(_QWORD *)(v21 + 8 * v22);
          if ( v25 != 0 )
            v24 = v25 + *(int *)(*(_QWORD *)(v25 + 8) + 4LL) + 8;
          else
            v24 = 0;
        }
        else
        {
          v24 = *(_QWORD *)(v21 + 8 * v22);
        }
        v56 = v24;
        if ( (unsigned __int8)sub_140F80250(a3, &v56, a5, 0) != 0 )
        {
          if ( v56 != 0 )
            v23 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v56 + 1688LL))(v56);
          else
            v23 = 0;
          *(_QWORD *)(v21 + 8 * v22) = v23;
          v17 = 1;
        }
        ++v22;
        v21 = *(_QWORD *)(a1 + 120);
      }
      while ( v22 < (*(_QWORD *)(a1 + 128) - v21) >> 3 );
    }
    v26 = *(_QWORD *)(a1 + 144);
    if ( *(_QWORD *)(a1 + 152) != v26 )
    {
      v27 = 0;
      do
      {
        if ( (a5 & 8) != 0 )
        {
          v30 = *(_QWORD *)(v26 + 8 * v27);
          if ( v30 != 0 )
            v29 = v30 + *(int *)(*(_QWORD *)(v30 + 8) + 4LL) + 8;
          else
            v29 = 0;
        }
        else
        {
          v29 = *(_QWORD *)(v26 + 8 * v27);
        }
        v56 = v29;
        if ( (unsigned __int8)sub_140F80250(a3, &v56, a5, 0) != 0 )
        {
          if ( v56 != 0 )
            v28 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v56 + 1688LL))(v56);
          else
            v28 = 0;
          *(_QWORD *)(v26 + 8 * v27) = v28;
          v17 = 1;
        }
        ++v27;
        v26 = *(_QWORD *)(a1 + 144);
      }
      while ( v27 < (*(_QWORD *)(a1 + 152) - v26) >> 3 );
    }
    if ( (v17 & 1) != 0 )
    {
      v31 = *(_QWORD **)(a1 + 104);
      v32 = (_QWORD *)sub_141751B70(*(_QWORD *)(a1 + 96), v31, 0);
      v33 = v32;
      if ( v32 != v31 )
      {
        while ( ++v32 != v31 )
        {
          if ( *v32 != 0 )
            *v33++ = *v32;
        }
      }
      if ( v33 != v31 )
      {
        v34 = *(_QWORD *)(a1 + 104) - (_QWORD)v31;
        sub_141758A00(v33, v31, v34);
        *(_QWORD *)(a1 + 104) = (char *)v33 + v34;
      }
      v35 = *(_QWORD **)(a1 + 128);
      v36 = (_QWORD *)sub_141751B70(*(_QWORD *)(a1 + 120), v35, 0);
      v37 = v36;
      if ( v36 != v35 )
      {
        while ( ++v36 != v35 )
        {
          if ( *v36 != 0 )
            *v37++ = *v36;
        }
      }
      if ( v37 != v35 )
      {
        v38 = *(_QWORD *)(a1 + 128) - (_QWORD)v35;
        sub_141758A00(v37, v35, v38);
        *(_QWORD *)(a1 + 128) = (char *)v37 + v38;
      }
      v39 = *(_QWORD **)(a1 + 152);
      v40 = (_QWORD *)sub_141751B70(*(_QWORD *)(a1 + 144), v39, 0);
      v41 = v40;
      if ( v40 != v39 )
      {
        while ( ++v40 != v39 )
        {
          if ( *v40 != 0 )
            *v41++ = *v40;
        }
      }
      if ( v41 != v39 )
      {
        v42 = *(_QWORD *)(a1 + 152) - (_QWORD)v39;
        sub_141758A00(v41, v39, v42);
        *(_QWORD *)(a1 + 152) = (char *)v41 + v42;
      }
    }
    v43 = *(_QWORD *)(a1 + 80) - *(_QWORD *)(a1 + 72);
    if ( v43 != 0 )
    {
      v44 = v43 >> 4;
      v45 = (v43 & 0xFFFFFFFFFFFFFFF0uLL) - 16;
      do
      {
        --v44;
        if ( (unsigned __int8)sub_141106260(v45 + *(_QWORD *)(a1 + 72), a3, a5) == 0 )
        {
          v46 = *(_QWORD *)(a1 + 72);
          v47 = *(_QWORD *)(a1 + 80);
          v48 = *(_QWORD *)(v46 + v45);
          v57 = *(_QWORD *)(v46 + v45 + 8);
          v56 = v48;
          v49 = *(_QWORD *)(v47 - 16);
          *(_QWORD *)(v46 + v45 + 8) = *(_QWORD *)(v47 - 8);
          *(_QWORD *)(v46 + v45) = v49;
          v50 = v56;
          *(_QWORD *)(v47 - 8) = v57;
          *(_QWORD *)(v47 - 16) = v50;
          *(_QWORD *)(a1 + 80) -= 16LL;
        }
        v45 -= 16LL;
      }
      while ( v44 != 0 );
    }
    v51 = *(_QWORD **)(a1 + 168);
    if ( v51 != nullptr )
    {
      v52 = v51[1] - *v51;
      if ( v52 != 0 )
      {
        v53 = v52 >> 3;
        do
        {
          v54 = *(_QWORD *)(**(_QWORD **)(a1 + 168) + 8 * v53 - 8);
          sub_140F7FD40(a3, v54, a5);
          sub_140F7EE40(a3, v54 + 8, *(_QWORD *)(a3 + 16), a5, 1, 0);
          --v53;
        }
        while ( v53 != 0 );
      }
    }
  }
  return 1;
}
