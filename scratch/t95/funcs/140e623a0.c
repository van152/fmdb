// THUNK ALIAS -> sub_143C27290 (jmp:0x140e623a0->0x143c27290)
__int64 __fastcall sub_143C27290(_QWORD *a1, char a2)
{
  char v2; // dl
  __int64 v3; // r8
  _QWORD *v4; // r12
  __int64 *v5; // rbp
  __int64 *v6; // rdi
  char v7; // bl
  __int64 *v8; // rcx
  __int64 v9; // rdx
  unsigned int v10; // eax
  int v11; // r13d
  unsigned int v12; // r14d
  char v14; // al
  unsigned int v15; // edx
  _QWORD *v16; // rcx
  _QWORD *v17; // rbx
  _QWORD *v18; // r15
  int v19; // edx
  int v20; // esi
  int v21; // r13d

  v2 = a2 ^ 1;
  v3 = 1049072;
  while ( 2 )
  {
    v4 = a1;
    v5 = (__int64 *)a1[35];
    v6 = (__int64 *)a1[36];
    if ( v5 == v6 )
    {
      return *(unsigned __int8 *)(a1[32] + 288LL);
    }
    else
    {
      v7 = v2;
      v8 = (__int64 *)a1[35];
      while ( 1 )
      {
        v9 = *v8;
        if ( *(_QWORD **)(*v8 + 8) == v4 )
        {
          v10 = *(unsigned __int8 *)(v9 + 48);
          if ( v10 <= 0x14 )
          {
            if ( _bittest((const int *)&v3, v10) )
              break;
          }
        }
        if ( ++v8 == v6 )
          goto LABEL_9;
      }
      a1 = *(_QWORD **)v9;
      v2 = 0;
      if ( a1 != nullptr )
        continue;
LABEL_9:
      v11 = *(unsigned __int8 *)(v4[32] + 288LL);
      if ( (v7 & 1) != 0 )
      {
        return *(unsigned __int8 *)(v4[32] + 288LL);
      }
      else
      {
        v14 = *(_BYTE *)(v4[32] + 288LL);
        v12 = (unsigned __int8)v14;
        do
        {
          v16 = (_QWORD *)*v5;
          v17 = *(_QWORD **)*v5;
          if ( v17 != nullptr )
          {
            v18 = (_QWORD *)v16[1];
            if ( v18 != nullptr )
            {
              v19 = *((unsigned __int8 *)v16 + 48);
              if ( (unsigned int)(v19 - 4) >= 5 && v19 != 20 )
              {
                v20 = v11;
                v21 = *((_DWORD *)v16 + 7);
                if ( (v21 & 0x400) != 0 && v18 == v4 )
                  v14 = (char)sub_140E623A0(*(_QWORD *)*v5, 0, v3) / 2;
                if ( (v21 & 0x10000) != 0 && v18 == v4 )
                  v14 = sub_140E623A0(v17, 0, v3);
                if ( (v21 & 0x40000) != 0 )
                {
                  v11 = v20;
                  if ( v17 == v4 )
                    v14 = sub_140E623A0(v18, 0, v3);
                }
                else
                {
                  v11 = v20;
                }
                v15 = (unsigned __int8)v12;
                v12 = (unsigned __int8)v12;
                if ( v14 > (char)v12 )
                  v12 = (unsigned __int8)v14;
                if ( v14 <= (char)v11 )
                  v12 = v15;
              }
            }
          }
          ++v5;
        }
        while ( v5 != v6 );
      }
    }
    return v12;
  }
}
