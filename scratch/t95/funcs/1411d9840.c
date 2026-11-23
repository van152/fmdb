__int64 **__fastcall sub_1411D9840(__int64 a1, _DWORD *a2, int a3, __int64 a4)
{
  int v8; // edi
  __int64 v9; // rsi
  __int64 **result; // rax
  __int64 *v11; // rbp
  __int64 *v12; // rax
  __int64 v13; // rax
  __int64 v14; // rbp
  __int64 v15; // rcx
  __int64 *v16; // rdx
  unsigned int v17; // ebp
  __int64 *v18; // rcx
  __int64 v19; // rcx
  char v20; // si
  _QWORD *v21; // rbx
  char v22; // r12
  __int64 v23; // rax
  int v24; // ecx
  unsigned __int64 v25; // rcx
  __int64 v26; // rbp
  __int64 v27; // rsi
  bool v28; // al
  __int64 v29; // rax
  _BYTE v30[24]; // [rsp+40h] [rbp-A8h] BYREF
  __int64 v31; // [rsp+58h] [rbp-90h]
  __int64 v32; // [rsp+60h] [rbp-88h]
  __int64 v33; // [rsp+68h] [rbp-80h]
  __int64 v34; // [rsp+90h] [rbp-58h]
  int v35; // [rsp+9Ch] [rbp-4Ch]
  char v36; // [rsp+A6h] [rbp-42h]

  v8 = 1049072;
  v9 = a1;
LABEL_2:
  result = *(__int64 ***)(v9 + 176);
  v11 = result[9];
  if ( v11 != nullptr )
  {
    if ( a4 != 0 )
      v20 = sub_1411D9B80(a1, a4);
    else
      v20 = -1;
    sub_14154FF10(v30);
    sub_141550040((unsigned int)v30, a1, a3, a4, 1);
    if ( a2 == nullptr )
    {
      v24 = -1;
      v22 = 0;
      v23 = 0;
LABEL_35:
      v35 = v24;
      v36 = v22;
      v34 = v23;
      sub_14155BF80((_DWORD)v11, 0, a1, a3, v20, (__int64)a2, 0);
      sub_1415554D0(v30, a1);
      if ( v31 != 0 )
      {
        v25 = v33 - v31;
        if ( v33 - v31 == -1 )
          v25 = *(unsigned int *)(v31 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v26 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v26) >> 3 > v25)
          && (v27 = *(_QWORD *)(v26 + 8 * v25)) != 0 )
        {
          MEMORY[0x1419475D8](v27 + 32, v31 - *(unsigned int *)(v27 + 120));
          v28 = *(_BYTE *)(v27 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v27 + 64)) != 0;
          if ( !v28 && *(_BYTE *)(v27 + 97) != 0 )
            sub_1412D33C0(v27);
        }
        else
        {
          MEMORY[0x141948990](v31 - *(unsigned int *)(qword_141ABD470 + 48));
        }
        v33 = 0;
        v32 = 0;
        v31 = 0;
      }
      return (__int64 **)sub_14083B0A0(v30);
    }
    v21 = (_QWORD *)(*(__int64 (__fastcall **)(_DWORD *, __int64, _QWORD))(*(_QWORD *)a2 + 1024LL))(a2, a1, 0);
    if ( v21 != nullptr )
      goto LABEL_29;
    if ( *(_BYTE *)(a1 + 186) != 0 || (v29 = sub_140E68C40(a1)) == 0 )
    {
      v22 = 0;
    }
    else
    {
      v22 = 0;
      v21 = (_QWORD *)(*(__int64 (__fastcall **)(_DWORD *, __int64, _QWORD))(*(_QWORD *)a2 + 1024LL))(a2, v29, 0);
      if ( v21 != nullptr )
      {
LABEL_29:
        v22 = (*(__int64 (__fastcall **)(_QWORD *))(*v21 + 80LL))(v21);
        v23 = v21[2];
LABEL_34:
        v24 = a2[2];
        goto LABEL_35;
      }
    }
    v23 = 0;
    goto LABEL_34;
  }
  if ( *(_BYTE *)(v9 + 186) == 0 )
  {
    v12 = *(__int64 **)(v9 + 24);
    if ( v12 == *(__int64 **)(v9 + 32)
      || (v13 = *v12) == 0
      || (v14 = *(_QWORD *)(v13 + 128)) == 0
      || (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)(v14 + *(int *)(*(_QWORD *)(v14 + 8) + 4LL) + 8) + 528LL))(a1) == 0
      || (result = (__int64 **)(*(__int64 (__fastcall **)(__int64))(*(_QWORD *)(v14
                                                                              + *(int *)(*(_QWORD *)(v14 + 8) + 4LL)
                                                                              + 8)
                                                                  + 1752LL))(v15)) == nullptr )
    {
      for ( result = *(__int64 ***)(v9 + 280); result != *(__int64 ***)(v9 + 288); ++result )
      {
        v16 = *result;
        if ( (*result)[1] == v9 )
        {
          v17 = *((unsigned __int8 *)v16 + 48);
          if ( v17 <= 0x14 )
          {
            if ( _bittest(&v8, v17) )
            {
              v9 = *v16;
              if ( *v16 != 0 )
              {
                result = *(__int64 ***)(v9 + 24);
                if ( result != *(__int64 ***)(v9 + 32) )
                {
                  v18 = *result;
                  if ( *result != nullptr )
                  {
                    if ( *((_BYTE *)v18 + 40) != 0 )
                    {
                      result = (__int64 **)sub_1411A41D0();
                      if ( result == nullptr )
                        return result;
                    }
                    else
                    {
                      result = (__int64 **)v18[16];
                      if ( result == nullptr )
                        return result;
                    }
                    v19 = (__int64)result + *((int *)result[1] + 1) + 8;
                    result = (__int64 **)(*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v19 + 1760LL))(v19);
                    if ( result != nullptr )
                      goto LABEL_2;
                  }
                }
              }
              return result;
            }
          }
        }
      }
    }
  }
  return result;
}
