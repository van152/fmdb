char __fastcall sub_141039B10(__int64 a1, int a2, __int64 **a3)
{
  __int64 v4; // rdx
  volatile signed __int32 **v5; // r13
  volatile signed __int32 *v6; // rax
  volatile signed __int32 *v7; // rcx
  volatile signed __int32 *v8; // rsi
  volatile signed __int32 *v9; // rsi
  __int64 **v10; // rax
  __int64 *v11; // rdi
  __int64 *v12; // r14
  __int64 v13; // r15
  __int64 v14; // rax
  unsigned __int8 v15; // dl
  __int64 v16; // rbx
  __int64 v17; // rsi
  __int64 v18; // rdi
  __int64 *v20; // rcx
  __int64 v21; // rax
  __int64 v22; // rcx
  __int64 v23; // r14
  __int64 v24; // r14
  __int64 v25; // r15
  __int64 v26; // rbx
  __int64 v27; // rdx
  __int64 *v28; // rax
  __int64 *v29; // rcx
  __int64 v30; // rax
  __int64 v31; // rcx
  __int64 v32; // rax
  __int64 v33; // r8
  __int64 v34; // rdi
  __int64 v35; // rsi
  unsigned __int64 v36; // rbp
  __int64 v37; // rcx
  _QWORD v38[9]; // [rsp+20h] [rbp-48h] BYREF

  if ( a2 > 1281977957 )
  {
    if ( a2 > 1282302323 )
    {
      if ( a2 == 1282302324 )
      {
        v18 = qword_141B5FDD0;
        sub_140FE7960(v38, a3, 1315856756);
        *(_QWORD *)(a1 + 40) = sub_14002F670(v18, v38);
        return 1;
      }
      if ( a2 == 1282635106 )
      {
        *(_WORD *)(a1 + 56) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        return 1;
      }
    }
    else
    {
      if ( a2 == 1281977958 )
      {
        *(_BYTE *)(a1 + 59) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        return 1;
      }
      if ( a2 == 1282302317 )
      {
        (*(void (__fastcall **)(__int64 *, _QWORD *))(**a3 + 128))(*a3, v38);
        v5 = (volatile signed __int32 **)(a1 + 24);
        if ( v5 != v38 )
        {
          v4 = v38[0];
          v6 = *v5;
          v7 = *v5 - 1;
          if ( *v5 == nullptr )
            v7 = nullptr;
          v8 = (volatile signed __int32 *)(v38[0] - 4LL);
          if ( v38[0] != 0 )
          {
            if ( v6 != nullptr && _InterlockedDecrement(v7) == 0 )
              sub_1412EC9A0(v7, v4);
            *v5 = nullptr;
            _InterlockedIncrement(v8);
            v9 = v8 + 1;
          }
          else
          {
            if ( v6 != nullptr && _InterlockedDecrement(v7) == 0 )
              sub_1412EC9A0(v7, v4);
            v9 = nullptr;
          }
          *v5 = v9;
        }
        v37 = v38[0];
        if ( v38[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38[0] - 4LL)) == 0 )
          sub_1412EC9A0(v37 - 4, v4);
        return 1;
      }
    }
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  }
  if ( a2 > 1281778028 )
  {
    if ( a2 == 1281778029 )
    {
      *(_WORD *)(a1 + 52) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      return 1;
    }
    if ( a2 == 1281847919 )
    {
      *(_WORD *)(a1 + 54) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      return 1;
    }
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  }
  if ( a2 == 1145392197 )
  {
    *(_WORD *)(a1 + 52) = -1;
    v10 = *(__int64 ***)(qword_141B5FDD0 + 128);
    v11 = *v10;
    v12 = v10[1];
    while ( v11 != v12 )
    {
      v13 = *v11;
      v14 = *(_QWORD *)(*v11 + 72);
      v15 = ((unsigned __int64)(*(_QWORD *)(*v11 + 80) - v14) >> 4) - 1;
      while ( (v15 & 0x80u) == 0 )
      {
        v17 = v15;
        if ( (*(_QWORD *)(*v11 + 80) - v14) >> 4 > (unsigned __int64)v15 )
          v16 = *(_QWORD *)(v14 + 16LL * v15);
        else
          v16 = 0;
        --v15;
        if ( v16 == a1 )
        {
          sub_141758A00(v14 + 16 * v17, v14 + 16 * v17 + 16, *(_QWORD *)(*v11 + 80) - (v14 + 16 * v17 + 16));
          *(_QWORD *)(v13 + 80) -= 16LL;
          break;
        }
      }
      ++v11;
    }
    v20 = *(__int64 **)(qword_141B5FDB0 + 128);
    v21 = *v20;
    v22 = v20[1];
    while ( v21 != v22 )
    {
      if ( *(_QWORD *)(*(_QWORD *)v21 + 48LL) == a1 )
        *(_QWORD *)(*(_QWORD *)v21 + 48LL) = 0;
      v21 += 8;
    }
    v23 = *(_QWORD *)(*(_QWORD *)(qword_141B5FE00 + 128) + 8LL) - **(_QWORD **)(qword_141B5FE00 + 128);
    if ( v23 == 0 )
      return 1;
    v24 = v23 >> 3;
    v25 = 0;
    while ( (int)v25 >= 0 )
    {
      v26 = 0;
      if ( qword_141B5FE00 != 0 )
      {
        if ( (_BYTE)word_141B60320 != 0
          || (v27 = *(_QWORD *)(qword_141B5FE00 + 96),
              (*(_QWORD *)(qword_141B5FE00 + 104) - v27) >> 3 <= (unsigned __int64)(unsigned int)v25) )
        {
          v29 = *(__int64 **)(qword_141B5FE00 + 128);
          v30 = *v29;
          v31 = v29[1] - *v29;
          if ( v31 == 0 || v31 >> 3 <= (unsigned __int64)(unsigned int)v25 )
            break;
          v28 = (__int64 *)(v30 + 8LL * (unsigned int)v25);
        }
        else
        {
          v28 = (__int64 *)(v27 + 8LL * (unsigned int)v25);
        }
        v26 = *v28;
      }
LABEL_55:
      v32 = *(_QWORD *)(v26 + 48);
      v33 = *(_QWORD *)(v26 + 56);
      if ( v33 != v32 )
      {
        v34 = 0;
        v35 = 0;
        v36 = 0;
        do
        {
          if ( *(_QWORD *)(v32 + v34) == a1 )
          {
            sub_141758A00(v32 + (v35 >> 28), v32 + (v35 >> 28) + 16, v33 - (v32 + (v35 >> 28) + 16));
            v32 = *(_QWORD *)(v26 + 48);
            v33 = *(_QWORD *)(v26 + 56) - 16LL;
            *(_QWORD *)(v26 + 56) = v33;
          }
          ++v36;
          v35 += 0x100000000LL;
          v34 += 16;
        }
        while ( v36 < (v33 - v32) >> 4 );
      }
      if ( ++v25 == v24 )
        return 1;
    }
    v26 = 0;
    goto LABEL_55;
  }
  if ( a2 != 1281648230 )
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  *(_BYTE *)(a1 + 60) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
  return 1;
}
