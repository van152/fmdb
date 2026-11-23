__int64 __fastcall sub_143C29780(__int64 a1, __int64 a2, __int64 a3)
{
  int v4; // eax
  __int64 v5; // rdi
  __int64 *v6; // rcx
  __int64 *v7; // rdx
  __int64 *v8; // rbx
  unsigned int v9; // esi
  char v10; // al
  __int64 *v11; // rcx
  __int16 v12; // ax
  __int64 v13; // rcx
  int v14; // ecx
  char v15; // al
  int v16; // ecx

  v4 = 1049072;
  while ( 2 )
  {
    v5 = a1;
    v6 = *(__int64 **)(a1 + 280);
    v7 = *(__int64 **)(v5 + 288);
    if ( v6 == v7 )
      goto LABEL_10;
    while ( 1 )
    {
      v8 = (__int64 *)*v6;
      if ( *(_QWORD *)(*v6 + 8) == v5 )
      {
        v9 = *((unsigned __int8 *)v8 + 48);
        if ( v9 <= 0x14 )
        {
          if ( _bittest(&v4, v9) )
            break;
        }
      }
      if ( ++v6 == v7 )
        goto LABEL_9;
    }
    a1 = *v8;
    if ( *v8 != 0 )
      continue;
    break;
  }
LABEL_9:
  *(_WORD *)a2 = 0;
  if ( v5 != 0 )
  {
LABEL_10:
    *(_BYTE *)(a2 + 1) = 0;
    LOBYTE(v7) = 1;
    v10 = sub_140E623A0(v5, v7, a3);
    *(_BYTE *)a2 = v10;
    if ( v10 <= 0 )
    {
      *(_BYTE *)(a2 + 1) = 1;
      v11 = *(__int64 **)(v5 + 24);
      v12 = 1500;
      if ( v11 != *(__int64 **)(v5 + 32) )
      {
        v13 = *v11;
        if ( v13 != 0 )
          v12 = *(_WORD *)(v13 + 168);
      }
      if ( *(char *)(v5 + 363) <= 0 )
      {
        v16 = v12;
        if ( *(char *)(v5 + 363) < 0 )
        {
          v15 = 10;
          if ( v16 <= 4499 )
          {
            v15 = 7;
            if ( v16 <= 2999 )
              v15 = 4 * (v16 >= 2000);
          }
        }
        else
        {
          v15 = 16;
          if ( v16 <= 5999 )
          {
            v15 = 13;
            if ( v16 <= 4499 )
            {
              v15 = 10;
              if ( v16 <= 2999 )
                v15 = 3 * (v16 >= 2000) + 4;
            }
          }
        }
      }
      else
      {
        v14 = v12;
        v15 = 16;
        if ( v14 <= 2999 )
        {
          v15 = 13;
          if ( v14 <= 1999 )
            v15 = 3 * (v14 >= 1000) + 7;
        }
      }
      *(_BYTE *)a2 = v15;
    }
  }
  return a2;
}
